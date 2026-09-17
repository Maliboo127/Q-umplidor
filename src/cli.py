"""
cli.py — Cliente de línea de comandos de Q-umplidor (RF-17).

Para el Hito 1 (núcleo local, sin red todavía) el CLI habla directamente
con un JobManager que vive en el mismo proceso. Cuando se implemente el
acceso remoto (Hito 3), esta capa se reemplaza por un cliente que habla
el protocolo de red contra el servicio, sin cambiar la semántica de las
operaciones (RF-19).
"""

from __future__ import annotations

import argparse
import json
import sys

from job_manager import JobManager, JobNotFound, InvalidJobRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qumplidor",
        description="Q-umplidor — gestor de trabajos para Linux.",
    )
    sub = parser.add_subparsers(dest="action", required=True)

    p_submit = sub.add_parser("submit", help="Enviar un trabajo.")
    p_submit.add_argument("cmd", nargs=argparse.REMAINDER,
                           help="Comando y argumentos a ejecutar, ej: -- echo hola")

    p_status = sub.add_parser("status", help="Consultar el estado de un trabajo.")
    p_status.add_argument("job_id")

    p_list = sub.add_parser("list", help="Listar trabajos.")
    p_list.add_argument("--state", default=None,
                         help="Filtrar por estado: QUEUED, RUNNING, SUCCEEDED, FAILED, CANCELED")

    p_cancel = sub.add_parser("cancel", help="Solicitar la cancelación de un trabajo.")
    p_cancel.add_argument("job_id")

    return parser


def run_cli(manager: JobManager, argv: list) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.action == "submit":
            command = args.cmd
            if command and command[0] == "--":
                command = command[1:]
            job_id = manager.submit(command)
            print(job_id)
            return 0

        if args.action == "status":
            print(json.dumps(manager.get_status(args.job_id), indent=2))
            return 0

        if args.action == "list":
            print(json.dumps(manager.list_jobs(args.state), indent=2))
            return 0

        if args.action == "cancel":
            print(json.dumps(manager.cancel(args.job_id), indent=2))
            return 0

    except InvalidJobRequest as e:
        print(f"Error: solicitud inválida — {e}", file=sys.stderr)
        return 2
    except JobNotFound:
        print(f"Error: no existe un trabajo con ese ID.", file=sys.stderr)
        return 3

    parser.print_help()
    return 1
