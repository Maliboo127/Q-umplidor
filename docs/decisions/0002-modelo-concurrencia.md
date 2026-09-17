# ADR-0002: Modelo de concurrencia y ejecución de trabajos

## Estado
**Aceptado** (confirmado en Hito 1, con prototipo funcional de referencia).

## Contexto y problema
El sistema deberá ejecutar múltiples trabajos en segundo plano sin bloquear la
atención de nuevas solicitudes (RF-04), respetar un máximo configurable de trabajos
simultáneos (RF-05, RNF-07), y mantener al menos 3 trabajos concurrentes en pruebas
controladas (RNF-04). Se necesita definir cómo el servicio administra: el proceso
hijo por trabajo, el hilo/loop que atiende solicitudes de clientes, y la cola quese
llena cuando se alcanza el límite (RF-03, RF-25).

## Alternativas consideradas

### Opción A — Un hilo supervisor + `subprocess.Popen` por trabajo
El servicio corre en un solo proceso con un hilo (o loop asíncrono) que acepta
solicitudes y lanza cada trabajo como proceso hijo independiente del SO. La
concurrencia real de los trabajos la da el sistema operativo (procesos), no el
lenguaje. Un hilo separado (o `waitpid`/`asyncio` no bloqueante) monitorea el fin
de cada hijo.
- Ventaja: modelo simple de razonar, sin condiciones de carrera complejas dentro
  del propio servicio.
- Riesgo: hay que cuidar el acceso concurrente a la cola/estado compartido entre
  el hilo que acepta solicitudes y el que detecta terminaciones.

### Opción B — Pool de procesos trabajadores con cola compartida
Un conjunto fijo de procesos "worker" (tamaño = límite de concurrencia) toma
trabajos de una cola compartida (ej. `multiprocessing.Queue`).
- Ventaja: el límite de concurrencia se aplica de forma estructural (no hay más
  workers que el límite).
- Riesgo: mayor complejidad de IPC entre el proceso principal y los workers para
  reportar estado/stdout de cada trabajo.

### Opción C — Un proceso por conexión de cliente (sin pool central)
Cada solicitud remota o local dispara su propio manejo aislado.
- Descartado preliminarmente: dificulta mantener una cola global y un límite de
  concurrencia consistente entre clientes (RF-05, RNF-07).

## Decisión
**Variante de la Opción A/B combinadas: pool fijo de hilos trabajadores
(tamaño = límite de concurrencia) que consumen una `queue.Queue` compartida,
lanzando cada trabajo con `subprocess.Popen`.** El límite de concurrencia
queda garantizado de forma estructural (nunca hay más hilos trabajadores que
el límite configurado), evitando la necesidad de un semáforo adicional como
en la Opción A pura. Confirmado con prueba automatizada
(`test_respects_concurrency_limit`) que lanza 4 trabajos con límite de 2 y
verifica que nunca haya más de 2 en RUNNING simultáneamente.

## Consecuencias
**Positivas:** menor superficie de error de sincronización.
**Negativas / riesgos:** requiere un mecanismo explícito de sincronización
(lock o cola thread-safe) para la cola de trabajos y la tabla de estados, dado que
será accedida desde el hilo que recibe solicitudes y el que detecta terminaciones
de procesos (relevante para RF-26, RNF-27).

## Requisitos afectados
RF-03, RF-04, RF-05, RF-25, RF-26, RNF-04, RNF-07, RNF-27.

## Evidencia / prototipo
`src/job_manager.py` (clase `JobManager`, método `_worker_loop`). Prueba
automatizada `test_respects_concurrency_limit` en
`tests/test_job_manager.py`, y pruebas de cancelación en cola
(`test_cancel_queued_job`) y en ejecución (`test_cancel_running_job`) que
validan la sincronización con `threading.RLock` sobre la cola y la tabla
de estados (relevante para RF-26, RNF-27).
