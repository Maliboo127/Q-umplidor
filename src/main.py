"""
main.py — Punto de entrada de Q-umplidor.

Modos disponibles en el Hito 1 (núcleo local):

  python3 src/main.py demo
      Ejecuta un flujo completo y reproducible dentro de un solo proceso:
      enviar varios trabajos, consultar su estado, listar, cancelar uno
      y mostrar el código de salida de los demás. Es la evidencia mínima
      pedida para RT-1 (envío, consulta, listado, cancelación, código de
      salida, manejo de comando inválido).

  python3 src/main.py <submit|status|list|cancel> ...
      Ejecuta una sola operación del CLI contra un JobManager nuevo.

LIMITACIÓN CONOCIDA (documentada para el equipo, ver docs/incidents/ o el
próximo ADR de persistencia): como todavía no existe un servicio en segundo
plano (daemon) ni persistencia entre procesos, cada invocación por separado
del CLI crea un JobManager nuevo y por lo tanto NO comparte estado con una
invocación anterior. Para consultar/listar/cancelar trabajos enviados
previamente es necesario hacerlo dentro de la misma ejecución (ver modo
`demo`) o esperar al Hito 2, donde se agrega persistencia y el servicio
corre de forma continua. Esta limitación debe explicarse en RT-1 si se
pregunta por qué `status` en una terminal nueva no encuentra el trabajo.
"""

from __future__ import annotations

import json
import sys
import time

from job_manager import JobManager
from cli import run_cli

# Portabilidad Windows/Linux: se usa el propio intérprete de Python
# (sys.executable) para los comandos de la demo en vez de binarios de
# Unix como echo/sleep/ls, que no existen como ejecutables en Windows.
# El despliegue final del servicio sigue apuntando a Linux (RNF-01); esto
# solo facilita correr la demo igual en cualquier máquina del equipo.
PY = sys.executable


def run_demo():
    print("=== Demo Q-umplidor — flujo local completo ===\n")

    manager = JobManager(max_concurrent=3, data_dir="./data")

    # RF-01: enviar varios trabajos
    job_ok = manager.submit([PY, "-c", "print('hola desde Q-umplidor')"])
    job_sleep = manager.submit([PY, "-c", "import time; time.sleep(2)"])
    job_fail = manager.submit([PY, "-c", "import sys; sys.exit(1)"])  # simula un fallo real
    print(f"Enviados: ok={job_ok}  sleep={job_sleep}  fail={job_fail}\n")

    # RF-02 / RNF-08: comando inválido no debe tumbar el servicio
    try:
        manager.submit([])
    except Exception as e:
        print(f"Rechazo esperado de comando vacío: {e}\n")

    try:
        manager.submit(["comando_que_no_existe_en_el_sistema"])
        print("Trabajo con binario inexistente enviado (fallará al ejecutar, no antes).\n")
    except Exception as e:
        print(f"(no debería llegar aquí): {e}")

    time.sleep(0.3)

    # RF-10: cancelar el trabajo largo mientras corre
    print(f"Cancelando {job_sleep} mientras está en ejecución...")
    print(json.dumps(manager.cancel(job_sleep), indent=2), "\n")

    time.sleep(1.0)

    # RF-09: listar todos los trabajos
    print("Listado completo de trabajos:")
    print(json.dumps(manager.list_jobs(), indent=2), "\n")

    # RF-08 / RF-07: estado y código de salida del trabajo exitoso
    print(f"Estado final de {job_ok}:")
    print(json.dumps(manager.get_status(job_ok), indent=2), "\n")

    print(f"Estado final de {job_fail} (esperado FAILED, exit_code != 0):")
    print(json.dumps(manager.get_status(job_fail), indent=2), "\n")

    manager.shutdown()
    print("=== Fin de la demo ===")


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 src/main.py [demo|submit|status|list|cancel] ...")
        sys.exit(1)

    if sys.argv[1] == "demo":
        run_demo()
        return

    manager = JobManager(max_concurrent=3, data_dir="./data")
    exit_code = run_cli(manager, sys.argv[1:])
    manager.shutdown()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
