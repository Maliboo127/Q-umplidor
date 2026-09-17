# ADR-0001: Lenguaje y runtime para Q-umplidor

## Estado
**Aceptado** (confirmado en Hito 1, con prototipo funcional de referencia).

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
**Python 3.** Se confirma tras implementar el núcleo local completo (envío,
ejecución como proceso separado, consulta, listado, cancelación y captura de
stdout/stderr) usando únicamente `subprocess`, `threading`, `queue` y `signal`
de la librería estándar — sin necesidad de dependencias externas para esta
etapa. El manejo de procesos y señales resultó directo y no presentó los
problemas de concurrencia que se temían (ver ADR-0002).

## Consecuencias
**Positivas (si se confirma Python):** desarrollo más rápido, más tiempo disponible
para verificación y documentación.
**Negativas / riesgos:** empaquetado y distribución del cliente/servicio requieren
más cuidado (venv, dependencias declaradas — RNF-02); mayor disciplina necesaria
para no introducir privilegios o dependencias no declaradas.

## Requisitos afectados
RF-04, RF-05, RNF-01, RNF-02, RNF-03, RNF-07.

## Evidencia / prototipo
Núcleo funcional en `src/job_manager.py`, `src/cli.py`, `src/main.py`.
12/12 pruebas unitarias en verde (`tests/test_job_manager.py`, ejecutables
con `bash verif/scripts/run_tests.sh`), cubriendo envío, ejecución, estados,
cancelación (en cola y en ejecución), captura separada de stdout/stderr,
comando inválido sin caída del servicio, y respeto del límite de
concurrencia.
