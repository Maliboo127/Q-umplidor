import subprocess
import sys
import time

siguiente_id = 1
trabajos = {}


def estado_trabajo(trabajo):
    """Devuelve el estado actual de un trabajo como texto."""
    codigo = trabajo["proceso"].poll()  # None = sigue corriendo

    if codigo is None:
        return "En ejecución"
    if trabajo["cancelado"]:
        return "Cancelado"
    if codigo == 0:
        return "Terminado"
    return f"Falló (código {codigo})"


def obtener_id(partes, comando):
    """Valida que el comando traiga un ID válido y que exista."""
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

        # Caso: sleep 10
        if len(partes) == 2:
            try:
                segundos = int(partes[1])
                time.sleep(segundos)
            except ValueError:
                print("sleep: invalid time interval")
            except KeyboardInterrupt:
                print()

        # Caso: sleep 10 &
        elif len(partes) == 3 and partes[2] == "&":
            try:
                segundos = int(partes[1])

                proceso = subprocess.Popen([
                    sys.executable,
                    "-c",
                    f"import time; time.sleep({segundos})"
                ])

                # Guarda el trabajo
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

    # Consulta el estado de un trabajo
    elif partes[0] == "estado":
        id_trabajo = obtener_id(partes, "estado")
        if id_trabajo is not None:
            trabajo = trabajos[id_trabajo]
            transcurrido = int(time.time() - trabajo["inicio"])
            print(f"[{id_trabajo}] {trabajo['comando']} -> {estado_trabajo(trabajo)} ({transcurrido}s)")

    
    else:
        print(f"{partes[0]}: comando no reconocido")
