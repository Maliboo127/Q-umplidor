# ADR-0003: Mecanismo de persistencia de trabajos

## Estado
Propuesta abierta — pendiente de resolución antes del Hito 2 (Concurrencia y
persistencia), aunque debe planearse desde ahora porque condiciona el formato de
datos que se use desde el Hito 1.

## Contexto y problema
El sistema deberá conservar metadatos y resultados mínimos después de reiniciar
el servicio (RF-12), recuperar el historial al arrancar y marcar coherentemente
los trabajos interrumpidos (RF-13, RNF-10), evitar dejar archivos a medio escribir
(RNF-11, RNF-28), y soportar al menos 500 registros sin pérdida de metadatos
(RNF-06).

## Alternativas consideradas

### Opción A — Archivos planos (JSON/JSON Lines por trabajo o por evento)
Cada trabajo se guarda como un archivo o línea independiente; se escribe con
patrón "escribir a temporal + rename atómico" para evitar estados parciales.
- Ventaja: cero dependencias externas, fácil de inspeccionar manualmente y de
  incluir como evidencia reproducible.
- Riesgo: hay que implementar a mano la atomicidad (RNF-11, RNF-28) y las
  consultas por filtro (RF-09) escalan peor a partir de cientos de registros.

### Opción B — SQLite
Una sola base de datos embebida con una tabla `jobs` (id, estado, tiempos,
código de salida, rutas de stdout/stderr).
- Ventaja: atomicidad y consistencia dadas por el motor (transacciones), consultas
  y filtros (RF-09) triviales con SQL, buen soporte para los ≥500 registros de
  RNF-06 y para el límite de 1s en consultas de RNF-05.
- Riesgo: una dependencia más que documentar y fijar versión (según doc. 04); el
  equipo debe aprender el manejo básico de transacciones para no violar RNF-27/28.

### Opción C — Persistencia en memoria + snapshot periódico a disco
Estado vive en memoria durante la ejecución; se vuelca a disco cada cierto
intervalo o al recibir señal de apagado.
- Descartado preliminarmente: una falla no controlada (no un apagado limpio)
  perdería trabajos completados entre snapshots, lo cual entra en conflicto
  directo con RF-12 y RNF-30/31.

## Decisión
**Pendiente.** Tendencia inicial hacia la **Opción B (SQLite)** por dar
atomicidad "gratis" para RNF-11/RNF-28 y facilitar las consultas de RF-08/RF-09
bajo el límite de tiempo de RNF-05, a confirmar con un prototipo simple de
escritura+lectura antes del Hito 2.

## Consecuencias
**Positivas:** menos código propio para garantizar atomicidad; consultas y
filtros más simples.
**Negativas / riesgos:** dependencia adicional a declarar y fijar versión
(estándares de repositorio, doc. 04); necesidad de manejar bien conexiones
concurrentes desde el hilo supervisor definido en ADR-0002.

## Requisitos afectados
RF-08, RF-09, RF-12, RF-13, RNF-05, RNF-06, RNF-10, RNF-11, RNF-28, RNF-31.

## Evidencia / prototipo
Pendiente: prueba de reinicio del servicio con trabajos en QUEUED/RUNNING antes
del corte, verificando que ninguno se reporte como RUNNING de forma falsa
(vinculada a TC-007).
