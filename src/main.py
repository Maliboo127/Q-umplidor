import subprocess
import sys
import time

siguiente_id = 1

while True:
    try:
        entrada = input("Q-umplidor> ").strip()
    except KeyboardInterrupt:
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

        # Caso: sleep 10 &
        elif len(partes) == 3 and partes[2] == "&":
            try:
                segundos = int(partes[1])

                subprocess.Popen([
                    sys.executable,
                    "-c",
                    f"import time; time.sleep({segundos})"
                ])

                print(f"ID: [{siguiente_id}]")
                siguiente_id += 1

            except ValueError:
                print("sleep: invalid time interval")
