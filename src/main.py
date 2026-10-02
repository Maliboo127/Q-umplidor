import subprocess
import sys
import time

siguiente_id = 1
trabajos = {}


def estado_trabajo(trabajo):
    """Devuelve el estado actual de un trabajo como texto (RF-06)."""
    codigo = trabajo["proceso"].poll()  # None = sigue corriendo

    if codigo is None:
        return "En ejecución"
    if trabajo["cancelado"]:
        return "Cancelado"
    if codigo == 0:
        return "Terminado"
    return f"Falló (código {codigo})"


def obtener_id(partes, comando):
    """Valida que el comando traiga un ID válido y que exista. Devuelve el ID o None."""
    if len(partes) != 2:
        print(f"Uso: {comando} <id>")
        return None

    try:
        id_trabajo = int(partes[1])
    except ValueError:
        print(f"{comando}: el ID debe ser un número")
        return None

    if id_trabajo not in trabajos:
        print(f"{comando}: no existe el trabajo [{id_trabajo}]")
        return None

    return id_trabajo


while True:
    try:
        entrada = input("Q-umplidor> ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        break

    partes = entrada.split()

    if len(partes) == 0:
        continue

    if partes[0] == "sleep":

        # Caso: sleep 10 (ejecución en primer plano, bloqueante)
        if len(partes) == 2:
            try:
                segundos = int(partes[1])
                time.sleep(segundos)
            except ValueError:
                print("sleep: invalid time interval")
            except KeyboardInterrupt:
                print()

        # Caso: sleep 10 &  -> RF-04: ejecutarlo como un proceso separado,
        # sin bloquear la atención de nuevas solicitudes.
        elif len(partes) == 3 and partes[2] == "&":
            try:
                segundos = int(partes[1])

                proceso = subprocess.Popen([
                    sys.executable,
                    "-c",
                    f"import time; time.sleep({segundos})"
                ])

                # RF-01/RF-06/RF-07: se guarda el trabajo con su ID,
                # comando, hora de inicio y bandera de cancelación
                # (esta última la usará quien implemente RF-10).
                trabajos[siguiente_id] = {
                    "proceso": proceso,
                    "comando": entrada,
                    "inicio": time.time(),
                    "cancelado": False,
                }

                print(f"ID: [{siguiente_id}]")
                siguiente_id += 1

            except ValueError:
                print("sleep: invalid time interval")

    # RF-09: listar trabajos con su estado
    elif partes[0] == "listar":
        if not trabajos:
            print("No hay trabajos registrados")
        else:
            print(f"{'ID':<4} {'ESTADO':<20} {'TIEMPO':<8} COMANDO")
            for id_trabajo, trabajo in trabajos.items():
                transcurrido = int(time.time() - trabajo["inicio"])
                print(
                    f"{id_trabajo:<4} {estado_trabajo(trabajo):<20} "
                    f"{transcurrido:<7}s {trabajo['comando']}"
                )

    # RF-07: obtener el código de salida de un trabajo
    elif partes[0] == "codigo":
        id_trabajo = obtener_id(partes, "codigo")
        if id_trabajo is not None:
            trabajo = trabajos[id_trabajo]
            codigo = trabajo["proceso"].poll()
            if codigo is None:
                print(f"codigo: el trabajo [{id_trabajo}] todavía está en ejecución, no tiene código de salida")
            else:
                print(f"codigo: el trabajo [{id_trabajo}] terminó con código de salida {codigo}")

    # RNF-08/09: un comando no reconocido no debe tumbar el servicio
    else:
        print(f"{partes[0]}: comando no reconocido")
