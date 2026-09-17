# Evidencia de la versión demostrada — Avance 01 (run-001)

| Campo | Valor |
|---|---|
| Fecha de ejecución | Ver commit en historial de git (Avance 01) |
| Componente probado | Núcleo local: `src/job_manager.py`, `src/cli.py`, `src/main.py` |
| Entorno | Windows (desarrollo, Python 3.13) + Linux (verificado en entorno auxiliar, Python 3.12) |
| Configuración | `max_concurrent=3` (demo), `max_concurrent=2` (pruebas unitarias) |
| Comando de verificación | `python -m pytest tests/ -v` |
| Comando de demostración | `python src/main.py demo` |
| Resultado de pruebas | **12/12 PASS** |
| Resultado de la demo | Flujo completo ejecutado sin errores: envío, ejecución, cancelación en ejecución, listado, consulta de estado y código de salida |

## Archivos de evidencia en esta carpeta

- `pytest-output.log` — salida completa de las 12 pruebas unitarias.
- `demo-output.log` — salida completa del flujo de demostración
  (`python src/main.py demo`), incluyendo el envío de varios trabajos, el
  rechazo de un comando vacío, la cancelación de un trabajo en ejecución,
  el listado completo y los estados/códigos de salida finales.

## Relación con RT-1

Esta evidencia respalda la demostración mínima exigida para el Hito 1
(doc. 06): *"ejecutar, consultar y finalizar un trabajo local"*, y sirve
de base para la defensa individual del recorrido de una solicitud (desde
`submit()` hasta el estado terminal) que cualquier integrante debe poder
explicar en la revisión técnica del 6 de octubre.
