# ADR-0001: Lenguaje y runtime para Q-umplidor

## Estado
Propuesta abierta — pendiente de resolución antes del Hito 1 (Núcleo local).

## Contexto y problema
Q-umplidor deberá ejecutar comandos en procesos separados, manejar señales, IPC,
concurrencia controlada (RF-04, RF-05, RNF-04, RNF-07) y persistencia recuperable
(RF-12, RF-13). El lenguaje elegido condiciona directamente qué tan simple o
compleja resulta cada una de esas partes, en especial el manejo de procesos y
concurrencia real (varios trabajos ejecutándose de verdad al mismo tiempo, no solo
de forma intercalada).

Actualmente el README declara Python como elección **provisional**, sin haberla
evaluado formalmente contra alternativas. Esta ADR formaliza esa evaluación.

## Alternativas consideradas

### Opción A — Python 3
- Rápido de escribir y depurar; buena librería estándar para procesos (`subprocess`),
  señales (`signal`) y sockets.
- El GIL no es un problema para RF-04/RF-05 porque la concurrencia deseada es entre
  **procesos hijos del SO**, no hilos de Python — el GIL solo afecta concurrencia
  dentro del propio intérprete.
- Empaquetado/distribución algo menos directo que un binario compilado.

### Opción B — C / C++
- Control fino sobre `fork`/`exec`, señales y descriptores; encaja de forma nativa
  con "programación de sistemas".
- Mayor curva de desarrollo y mayor riesgo de errores de memoria/concurrencia bajo
  presión de tiempo académico.

### Opción C — Go
- Concurrencia nativa (goroutines) y buen soporte de red; compila a binario único,
  lo que facilita RNF-02 (build reproducible).
- Menor experiencia previa del equipo; curva de aprendizaje adicional.

## Decisión
**Pendiente.** El equipo se inclina provisionalmente por **Python 3**, priorizando
velocidad de desarrollo dado el tamaño del equipo y el calendario académico, pero
esta decisión debe confirmarse antes de cerrar el Hito 1, después de una prueba
mínima de manejo de procesos y señales en Python.

## Consecuencias
**Positivas (si se confirma Python):** desarrollo más rápido, más tiempo disponible
para verificación y documentación.
**Negativas / riesgos:** empaquetado y distribución del cliente/servicio requieren
más cuidado (venv, dependencias declaradas — RNF-02); mayor disciplina necesaria
para no introducir privilegios o dependencias no declaradas.

## Requisitos afectados
RF-04, RF-05, RNF-01, RNF-02, RNF-03, RNF-07.

## Evidencia / prototipo
Pendiente: se agregará un script mínimo de `fork`/`subprocess` + captura de
señal como evidencia antes de confirmar esta ADR.
