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
    """Valida que el comando traiga un ID válido y que exista. Devuelve el ID o None."""
    if len(partes) == 1:
        print(f"{comando}: falta el ID del trabajo. Uso: {comando} <id>")
        return None
    if len(partes) != 2:
        print(f"{comando}: argumentos incorrectos. Uso: {comando} <id>")
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

    if partes[0] == "help":
        if len(partes) != 1:
            print("help: no acepta argumentos. Uso: help")
            continue
        print("Comandos disponibles:")
        print("  sleep <segundos>    Ejecutar una espera en primer plano.")
        print("  sleep <segundos> &  Ejecutar un trabajo en segundo plano.")
        print("  estado <id>         Consultar el estado de un trabajo.")
        print("  listar              Listar los trabajos registrados.")
        print("  codigo <id>         Consultar el código de salida.")
        print("  cancelar <id>       Cancelar un trabajo.")
        print("  help                Mostrar esta ayuda.")

    elif partes[0] == "sleep":
        if len(partes) == 1 or partes == ["sleep", "&"]:
            print("sleep: faltan los segundos. Uso: sleep <segundos> o sleep <segundos> &")
            continue

        if len(partes) not in (2, 3) or (len(partes) == 3 and partes[2] != "&"):
            print("sleep: argumentos incorrectos. Uso: sleep <segundos> o sleep <segundos> &")
            continue
        try:
            segundos = int(partes[1])
            if segundos < 0:
                raise ValueError
        except ValueError:
            print("sleep: los segundos deben ser un entero no negativo")
            continue

        # Caso: sleep 10
        if len(partes) == 2:
            try:
                time.sleep(segundos)
            except (ValueError, OverflowError):
                print("sleep: invalid time interval")
            except KeyboardInterrupt:
                print()

        # Caso: sleep 10 &
        elif len(partes) == 3 and partes[2] == "&":
            try:

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

            except (ValueError, OverflowError):
                print("sleep: invalid time interval")

    # Consulta el estado de un trabajo
    elif partes[0] == "estado":
        id_trabajo = obtener_id(partes, "estado")
        if id_trabajo is not None:
            trabajo = trabajos[id_trabajo]
            transcurrido = int(time.time() - trabajo["inicio"])
            print(f"[{id_trabajo}] {trabajo['comando']} -> {estado_trabajo(trabajo)} ({transcurrido}s)")

    # Listar los trabajos
    elif partes[0] == "listar":
        if len(partes) != 1:
            print("listar: no acepta argumentos. Uso: listar")
            continue
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

    # Obtener el código de salida de un trabajo
    elif partes[0] == "codigo":
        if len(partes) == 1:
            print("codigo: falta el ID del trabajo. Uso: codigo <id>")
        elif len(partes) != 2:
            print("codigo: argumentos incorrectos. Uso: codigo <id>")
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

    # Solicitud de cancelación
    elif partes[0] == "cancelar":
        id_trabajo = obtener_id(partes, "cancelar")
        if id_trabajo is not None:
            trabajo = trabajos[id_trabajo]
            proceso = trabajo["proceso"]

            if proceso.poll() is not None:
                print(f"cancelar: el trabajo [{id_trabajo}] ya terminó ({estado_trabajo(trabajo)})")
            else:
                trabajo["cancelado"] = True
                proceso.terminate()  # Envía SIGTERM
                try:
                    proceso.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proceso.kill()  # Envía SIGKILL si no respondió
                    proceso.wait()
                print(f"Trabajo [{id_trabajo}] cancelado")

    # Manejar comandos inválidos sin terminar el servicio 
    else:
        print(f"{partes[0]}: comando no reconocido")
