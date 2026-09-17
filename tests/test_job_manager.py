"""
test_job_manager.py — Primeros casos de prueba unitarios de Q-umplidor.

Corresponden a TC-001 (enviar trabajo válido), TC-003 (estados y tiempos),
TC-005 (cancelar en cola y ejecución), TC-006 (captura de stdout/stderr y
código de salida), y validación de RF-02 / RNF-08 (comando inválido no
debe tumbar el servicio).

Ejecutar con:  python3 -m pytest tests/ -v
"""

import sys
import os
import time
import tempfile
import shutil
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from job_manager import (  # noqa: E402
    JobManager,
    InvalidJobRequest,
    JobNotFound,
    QUEUED,
    RUNNING,
    SUCCEEDED,
    FAILED,
    CANCELED,
)

# Portabilidad Windows/Linux (ver docs/incidents/ o ADR relacionado):
# comandos como "true", "false", "sleep", "echo" son binarios de Unix y no
# existen como ejecutables reales en Windows (no hay true.exe/sleep.exe).
# Usamos el propio intérprete de Python (sys.executable), disponible en
# ambos sistemas operativos, como comando de prueba portable. El sistema
# de producción final sigue apuntando a Linux (RNF-01); esto es solo para
# que las pruebas automatizadas corran igual en cualquier máquina de
# desarrollo del equipo.
PY = sys.executable
CMD_TRUE = [PY, "-c", "pass"]
CMD_FALSE = [PY, "-c", "import sys; sys.exit(1)"]


def cmd_sleep(seconds):
    return [PY, "-c", f"import time; time.sleep({seconds})"]


class TestJobManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix="qumplidor_test_")
        self.manager = JobManager(max_concurrent=2, data_dir=self.tmp_dir)

    def tearDown(self):
        self.manager.shutdown()
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    # TC-001: enviar trabajo válido devuelve un ID único
    def test_submit_returns_unique_id(self):
        id1 = self.manager.submit([PY, "-c", "print('a')"])
        id2 = self.manager.submit([PY, "-c", "print('b')"])
        self.assertNotEqual(id1, id2)
        self.assertTrue(len(id1) > 0)

    # RF-02 / RNF-08: comando vacío se rechaza sin tumbar el servicio
    def test_submit_rejects_empty_command(self):
        with self.assertRaises(InvalidJobRequest):
            self.manager.submit([])

    def test_submit_rejects_non_list(self):
        with self.assertRaises(InvalidJobRequest):
            self.manager.submit("echo hola")  # str en vez de list

    # TC-003: estados y tiempos
    def test_job_reaches_succeeded_with_exit_code_zero(self):
        job_id = self.manager.submit(CMD_TRUE)  # comando que siempre retorna 0
        self._wait_for_terminal(job_id)
        status = self.manager.get_status(job_id)
        self.assertEqual(status["state"], SUCCEEDED)
        self.assertEqual(status["exit_code"], 0)
        self.assertIsNotNone(status["started_at"])
        self.assertIsNotNone(status["finished_at"])

    def test_job_reaches_failed_with_nonzero_exit_code(self):
        job_id = self.manager.submit(CMD_FALSE)  # comando que siempre retorna 1
        self._wait_for_terminal(job_id)
        status = self.manager.get_status(job_id)
        self.assertEqual(status["state"], FAILED)
        self.assertEqual(status["exit_code"], 1)

    # RNF-08: comando inexistente falla de forma controlada, no tumba el servicio
    def test_nonexistent_binary_marks_job_failed_not_crash(self):
        job_id = self.manager.submit(["binario_que_no_existe_xyz"])
        self._wait_for_terminal(job_id)
        status = self.manager.get_status(job_id)
        self.assertEqual(status["state"], FAILED)
        self.assertIsNotNone(status["error"])
        # El manager debe seguir vivo y aceptar más trabajos:
        job_id2 = self.manager.submit([PY, "-c", "print('sigo vivo')"])
        self._wait_for_terminal(job_id2)
        self.assertEqual(self.manager.get_status(job_id2)["state"], SUCCEEDED)

    # TC-005: cancelar en ejecución
    def test_cancel_running_job(self):
        job_id = self.manager.submit(cmd_sleep(5))
        time.sleep(0.3)  # dejar que arranque
        result = self.manager.cancel(job_id)
        self.assertEqual(result["state"], CANCELED)

    # TC-005: cancelar en cola (antes de que empiece a correr)
    def test_cancel_queued_job(self):
        # Saturamos los 2 slots con trabajos largos para forzar que el
        # siguiente se quede en cola.
        self.manager.submit(cmd_sleep(2))
        self.manager.submit(cmd_sleep(2))
        queued_id = self.manager.submit([PY, "-c", "print('nunca deberia correr')"])
        result = self.manager.cancel(queued_id)
        self.assertEqual(result["state"], CANCELED)

    # TC-006: captura separada de stdout y stderr
    def test_stdout_and_stderr_are_captured_separately(self):
        job_id = self.manager.submit(
            [PY, "-c", "import sys; print('salida'); print('error', file=sys.stderr)"]
        )
        self._wait_for_terminal(job_id)
        status = self.manager.get_status(job_id)
        with open(status["stdout_path"]) as f:
            self.assertIn("salida", f.read())
        with open(status["stderr_path"]) as f:
            self.assertIn("error", f.read())

    # RF-09: listar con filtro por estado
    def test_list_filters_by_state(self):
        ok_id = self.manager.submit(CMD_TRUE)
        fail_id = self.manager.submit(CMD_FALSE)
        self._wait_for_terminal(ok_id)
        self._wait_for_terminal(fail_id)

        succeeded = self.manager.list_jobs(state_filter=SUCCEEDED)
        failed = self.manager.list_jobs(state_filter=FAILED)

        self.assertTrue(any(j["id"] == ok_id for j in succeeded))
        self.assertTrue(any(j["id"] == fail_id for j in failed))

    # RF-08: consultar un ID inexistente
    def test_status_of_unknown_job_raises(self):
        with self.assertRaises(JobNotFound):
            self.manager.get_status("id-que-no-existe")

    # RF-05: no se exceden los trabajos simultáneos configurados
    def test_respects_concurrency_limit(self):
        # max_concurrent=2 en setUp; lanzamos 4 trabajos largos y verificamos
        # que nunca haya más de 2 en RUNNING al mismo tiempo.
        ids = [self.manager.submit(cmd_sleep(1)) for _ in range(4)]
        time.sleep(0.3)
        running = [j for j in self.manager.list_jobs() if j["state"] == RUNNING]
        self.assertLessEqual(len(running), 2)
        for job_id in ids:
            self._wait_for_terminal(job_id, timeout=5)

    # ---------------------------------------------------------------- #
    def _wait_for_terminal(self, job_id, timeout=3):
        deadline = time.time() + timeout
        while time.time() < deadline:
            status = self.manager.get_status(job_id)
            if status["state"] in (SUCCEEDED, FAILED, CANCELED):
                return status
            time.sleep(0.05)
        self.fail(f"El trabajo {job_id} no terminó dentro de {timeout}s")


if __name__ == "__main__":
    unittest.main()
