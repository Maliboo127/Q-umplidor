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
    if codigo == 0:
        return "Terminado"
    return f"Falló (código {codigo})"


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

        # Caso: sleep 10 &  -> RF-04: ejecutarlo como un proceso separado,
        # sin bloquear la atención de nuevas solicitudes.
        if len(partes) == 3 and partes[2] == "&":
            try:
                segundos = int(partes[1])

                proceso = subprocess.Popen([
                    sys.executable,
                    "-c",
                    f"import time; time.sleep({segundos})"
                ])

                # RF-01/RF-06/RF-07: se guarda el trabajo con su ID,
                # comando y hora de inicio
                trabajos[siguiente_id] = {
                    "proceso": proceso,
                    "comando": entrada,
                    "inicio": time.time(),
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
        if len(partes) != 2:
            print("Uso: codigo <id>")
        else:
            try:
                id_trabajo = int(partes[1])
                if id_trabajo not in trabajos:
                    print(f"codigo: no existe el trabajo [{id_trabajo}]")
                else:
                    trabajo = trabajos[id_trabajo]
                    codigo = trabajo["proceso"].poll()
                    if codigo is None:
                        print(f"codigo: el trabajo [{id_trabajo}] todavía está en ejecución, no tiene código de salida")
                    else:
                        print(f"codigo: el trabajo [{id_trabajo}] terminó con código de salida {codigo}")
            except ValueError:
                print("codigo: el ID debe ser un número")

    # RNF-08/09: un comando no reconocido no debe tumbar el servicio
    else:
        print(f"{partes[0]}: comando no reconocido")
