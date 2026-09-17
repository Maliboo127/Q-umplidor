"""
job_manager.py — Núcleo de Q-umplidor.

Implementa RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09,
RF-10, RF-11 (subconjunto correspondiente al Hito 1 — núcleo local).

Decisión de arquitectura (ver docs/decisions/0002-modelo-concurrencia.md):
un pool fijo de hilos trabajadores consume una cola thread-safe (queue.Queue)
y lanza cada trabajo como un proceso hijo independiente del SO
(subprocess.Popen). El límite de concurrencia queda garantizado de forma
estructural por el número de hilos del pool.
"""

from __future__ import annotations

import json
import os
import queue
import signal
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# Estados del trabajo (RF-06)
QUEUED = "QUEUED"
RUNNING = "RUNNING"
SUCCEEDED = "SUCCEEDED"
FAILED = "FAILED"
CANCELED = "CANCELED"

TERMINAL_STATES = {SUCCEEDED, FAILED, CANCELED}


@dataclass
class Job:
    id: str
    command: list
    state: str = QUEUED
    submitted_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    exit_code: Optional[int] = None
    error: Optional[str] = None
    stdout_path: Optional[str] = None
    stderr_path: Optional[str] = None
    pid: Optional[int] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        # El objeto Popen no es serializable; nunca se guarda en el dataclass.
        return d


class InvalidJobRequest(ValueError):
    """RF-02: solicitud vacía, mal formada o no autorizada."""


class JobNotFound(KeyError):
    pass


class JobManager:
    """
    Administra el ciclo de vida de los trabajos.

    max_concurrent: límite configurable de trabajos simultáneos (RF-05).
    data_dir: directorio donde se guarda stdout/stderr de cada trabajo (RF-16).
    """

    def __init__(self, max_concurrent: int = 3, data_dir: str = "./data"):
        if max_concurrent < 1:
            raise ValueError("max_concurrent debe ser >= 1")

        self.max_concurrent = max_concurrent
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self._jobs: dict[str, Job] = {}
        self._procs: dict[str, subprocess.Popen] = {}
        self._lock = threading.RLock()
        self._queue: "queue.Queue[str]" = queue.Queue()
        self._shutting_down = False

        self._workers = [
            threading.Thread(target=self._worker_loop, daemon=True, name=f"worker-{i}")
            for i in range(max_concurrent)
        ]
        for w in self._workers:
            w.start()

    # ---------------------------------------------------------------- #
    # RF-01 / RF-02: envío y validación
    # ---------------------------------------------------------------- #
    def submit(self, command: list) -> str:
        if self._shutting_down:
            raise InvalidJobRequest("El servicio está cerrando; no acepta trabajos nuevos.")

        if not isinstance(command, list) or len(command) == 0:
            raise InvalidJobRequest("El comando no puede estar vacío ni tener formato inválido.")

        if not all(isinstance(part, str) and part.strip() != "" for part in command):
            raise InvalidJobRequest("Todos los argumentos del comando deben ser texto no vacío.")

        job_id = str(uuid.uuid4())
        job_dir = self.data_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        job = Job(
            id=job_id,
            command=command,
            stdout_path=str(job_dir / "stdout.log"),
            stderr_path=str(job_dir / "stderr.log"),
        )

        with self._lock:
            self._jobs[job_id] = job

        self._queue.put(job_id)
        return job_id

    # ---------------------------------------------------------------- #
    # RF-04 / RF-11: ejecución como proceso separado, captura separada
    # ---------------------------------------------------------------- #
    def _worker_loop(self):
        while True:
            job_id = self._queue.get()
            if job_id is None:  # señal de apagado
                self._queue.task_done()
                return
            self._run_job(job_id)
            self._queue.task_done()

    def _run_job(self, job_id: str):
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None or job.state == CANCELED:
                return  # se canceló mientras estaba en cola
            job.state = RUNNING
            job.started_at = time.time()

        try:
            with open(job.stdout_path, "wb") as out, open(job.stderr_path, "wb") as err:
                proc = subprocess.Popen(job.command, stdout=out, stderr=err)
                with self._lock:
                    # Pudo haberse cancelado justo antes de este punto.
                    if self._jobs[job_id].state == CANCELED:
                        proc.terminate()
                    self._procs[job_id] = proc
                    job.pid = proc.pid

                returncode = proc.wait()

            with self._lock:
                if job.state == CANCELED:
                    pass  # ya se marcó por cancel(); no sobrescribir
                else:
                    job.exit_code = returncode
                    job.state = SUCCEEDED if returncode == 0 else FAILED
                job.finished_at = time.time()
                self._procs.pop(job_id, None)

        except FileNotFoundError as e:
            # RF-02 / RNF-08: comando inválido no debe tumbar el servicio.
            with self._lock:
                job.state = FAILED
                job.error = f"Comando no encontrado: {e}"
                job.finished_at = time.time()
        except Exception as e:  # noqa: BLE001 — aislamiento de fallo (RNF-09)
            with self._lock:
                job.state = FAILED
                job.error = f"Error inesperado al ejecutar el trabajo: {e}"
                job.finished_at = time.time()

    # ---------------------------------------------------------------- #
    # RF-08: consultar estado
    # ---------------------------------------------------------------- #
    def get_status(self, job_id: str) -> dict:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                raise JobNotFound(job_id)
            return job.to_dict()

    # ---------------------------------------------------------------- #
    # RF-09: listar con filtro por estado
    # ---------------------------------------------------------------- #
    def list_jobs(self, state_filter: Optional[str] = None) -> list:
        with self._lock:
            jobs = list(self._jobs.values())
        if state_filter:
            jobs = [j for j in jobs if j.state == state_filter]
        return [j.to_dict() for j in sorted(jobs, key=lambda j: j.submitted_at)]

    # ---------------------------------------------------------------- #
    # RF-10: cancelación en cola o en ejecución
    # ---------------------------------------------------------------- #
    def cancel(self, job_id: str) -> dict:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                raise JobNotFound(job_id)

            if job.state in TERMINAL_STATES:
                return job.to_dict()  # ya terminó; RF-26 semántica idempotente

            if job.state == QUEUED:
                job.state = CANCELED
                job.finished_at = time.time()
                return job.to_dict()

            if job.state == RUNNING:
                job.state = CANCELED
                job.finished_at = time.time()
                proc = self._procs.get(job_id)

        # Enviar la señal fuera del lock para no bloquear otros hilos.
        if job.state == CANCELED and job_id in self._procs:
            try:
                proc = self._procs[job_id]
                proc.send_signal(signal.SIGTERM)
            except (ProcessLookupError, KeyError):
                pass

        with self._lock:
            return self._jobs[job_id].to_dict()

    # ---------------------------------------------------------------- #
    # RF-15: cierre controlado
    # ---------------------------------------------------------------- #
    def shutdown(self):
        with self._lock:
            self._shutting_down = True
        for _ in self._workers:
            self._queue.put(None)
        for w in self._workers:
            w.join(timeout=5)
