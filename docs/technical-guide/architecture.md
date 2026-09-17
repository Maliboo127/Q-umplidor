# Arquitectura inicial — Q-umplidor (Hito 1: núcleo local)

## Visión general

En esta etapa, Q-umplidor corre como un **único proceso Python** que contiene
toda la lógica de administración de trabajos. Ese proceso lanza cada trabajo
enviado como un **proceso hijo del sistema operativo** independiente
(`subprocess.Popen`), nunca dentro del propio intérprete de Python.

```
┌─────────────────────────────────────────────┐
│              Proceso Q-umplidor              │
│                                               │
│   CLI (src/cli.py)                           │
│        │                                     │
│        ▼                                     │
│   JobManager (src/job_manager.py)            │
│        │                                     │
│        ├── cola thread-safe (queue.Queue)    │
│        │                                     │
│        └── pool de N hilos trabajadores      │
│                 │        │        │          │
│                 ▼        ▼        ▼          │
│            Popen()   Popen()   Popen()       │
└────────────┼──────────┼──────────┼───────────┘
             ▼          ▼          ▼
        proceso     proceso     proceso
         hijo #1     hijo #2     hijo #3
      (comando)   (comando)   (comando)
```

## Modelo de procesos

- **Un solo proceso Q-umplidor** administra todo (por ahora — ver
  *Limitaciones conocidas* más abajo).
- Cada trabajo enviado se ejecuta como su **propio proceso del sistema
  operativo**, aislado del proceso Q-umplidor y de los demás trabajos
  (RF-04, RNF-09).
- El límite de trabajos simultáneos (RF-05) se garantiza de forma
  estructural: existen exactamente `max_concurrent` hilos trabajadores, y
  nunca puede haber más procesos hijo corriendo que hilos trabajadores.

## Modelo de concurrencia (hilos, no procesos, para el orquestador)

- El **orquestador** (JobManager) usa un **pool fijo de hilos** de Python
  (`threading.Thread`), no procesos del SO, para consumir trabajos de la
  cola.
- La **cola de trabajos** es un `queue.Queue`, estructura nativa de Python
  ya thread-safe.
- La **tabla de estados de trabajos** (diccionario en memoria) se protege
  con un `threading.RLock` para evitar condiciones de carrera cuando varios
  hilos leen/escriben al mismo tiempo (relevante para RF-26, RNF-27).
- Cada hilo trabajador, al tomar un trabajo de la cola, lanza el proceso
  hijo real con `subprocess.Popen` y se queda bloqueado en `proc.wait()`
  hasta que termina — ese hilo no vuelve a estar libre hasta entonces.

*(Justificación completa y alternativas descartadas en
[ADR-0002](../decisions/0002-modelo-concurrencia.md).)*

## IPC (comunicación entre procesos)

En el Hito 1 **no hay comunicación entre procesos** todavía, porque todo
corre en un solo proceso Q-umplidor:

- El proceso Q-umplidor no habla con los procesos hijo más que para:
  - lanzarlos (`Popen`)
  - esperar su terminación (`wait()`)
  - enviarles una señal si se cancelan (`SIGTERM`)
  - leer su código de salida
- **stdout y stderr** de cada trabajo se redirigen directamente a archivos
  en disco (`data/<job_id>/stdout.log` y `stderr.log`), no se leen en
  memoria ni se transmiten por ningún canal — así se garantiza que no se
  mezclen (RF-11) sin necesidad de pipes complejos.

La comunicación **cliente ↔ servicio** (necesaria para que `status`/`list`
funcionen entre invocaciones separadas del CLI) es el IPC real pendiente,
ver *Limitaciones conocidas*.

## Manejo de señales

- **Cancelación (RF-10):** al cancelar un trabajo en ejecución, el
  JobManager envía `SIGTERM` al proceso hijo (`proc.send_signal`). No se
  usa `SIGKILL` todavía — la política de escalamiento a `SIGKILL` si el
  proceso no responde (RF-30) queda pendiente para un hito posterior.
- Un trabajo cancelado mientras estaba en `QUEUED` (nunca llegó a lanzarse)
  simplemente se marca `CANCELED` sin enviar ninguna señal, porque no existe
  proceso hijo todavía.

## Estrategia de errores

Cada error se atrapa **a nivel de trabajo individual**, nunca deja caer el
proceso Q-umplidor completo (RNF-08, RNF-09):

| Situación | Manejo |
|---|---|
| Comando vacío o mal formado | Se rechaza en `submit()` antes de encolar (`InvalidJobRequest`) |
| Binario que no existe | `FileNotFoundError` capturada dentro del hilo trabajador → trabajo pasa a `FAILED` con mensaje de diagnóstico |
| Cualquier otra excepción durante la ejecución | Capturada de forma genérica → trabajo pasa a `FAILED`, el hilo trabajador sigue vivo y toma el siguiente trabajo de la cola |
| Consulta de un ID que no existe | Excepción `JobNotFound`, capturada por el CLI y mostrada como error legible |

## Configuración

Por ahora, configurable solo por parámetros del constructor de
`JobManager` (no por archivo ni variables de entorno todavía — pendiente
para completar RF-16):

- `max_concurrent`: límite de trabajos simultáneos (default: 3)
- `data_dir`: carpeta donde se guardan stdout/stderr de cada trabajo
  (default: `./data`)

## Amenazas y límites conocidos (preliminar)

- Sin acceso remoto todavía: superficie de ataque mínima, todo corre
  localmente bajo el usuario que ejecuta el proceso.
- No se valida que el comando enviado pertenezca a una lista permitida —
  cualquier binario del `PATH` del sistema puede ejecutarse. Esto es
  aceptable para el Hito 1 (cliente y servicio corren como el mismo
  usuario, sin frontera de confianza todavía), pero deberá revisarse antes
  del Hito 3 (acceso remoto).
- Sin límite de recursos (CPU/memoria) por trabajo todavía.

## Limitaciones conocidas de esta etapa

1. **No hay servicio en segundo plano (daemon) todavía.** Cada invocación
   del CLI (`python src/main.py submit|status|list|cancel`) crea un
   `JobManager` nuevo en memoria. Por eso `status`/`list` no encuentran
   trabajos enviados en una invocación anterior — solo funcionan dentro de
   la misma ejecución (ver el modo `demo` en `src/main.py`).
2. **Sin persistencia** (RF-12, RF-13 — planeadas para Hito 2).
3. **Sin protocolo de red** (RF-18 a RF-22 — planeadas para Hito 3).
4. **Sin política de escalamiento de cancelación** (RF-30 — planeada junto
   con la persistencia/recuperación en un hito posterior).

Estas limitaciones son intencionales y corresponden al alcance exacto del
Hito 1 según doc. 06 ("no se requiere todavía la operación remota").
