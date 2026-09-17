# Matriz de trazabilidad — Q-umplidor

Estado: **en construcción** (Avance 01). Sin huecos: incluye RF-01..RF-30 y
RNF-01..RNF-34 en su totalidad, tal como exige el Plan de Verificación (doc. 05).

Resumen: **16 de 64** requisitos con resultado PASS hasta el
momento (correspondiente al alcance del Hito 1 — núcleo local). El resto
está marcado Pendiente porque corresponde a etapas posteriores (persistencia,
red, seguridad) o a casos de prueba formales todavía no escritos como
TC-XXX independientes (se usó evidencia directa de las pruebas unitarias
existentes mientras tanto).

| Req ID | Descripción breve | Prioridad | Método | Caso(s) | Evidencia | Resultado | Defecto/Excepción |
|---|---|---|---|---|---|---|---|
| RF-01 | Enviar comando con argumentos y devolver ID único | Alta | Prueba | TC-001 | tests/test_job_manager.py::test_submit_returns_unique_id | PASS | - |
| RF-02 | Validar y rechazar entradas vacías/mal formadas | Alta | Prueba | TC-001 | tests/test_job_manager.py::test_submit_rejects_empty_command, test_submit_rejects_non_list | PASS | - |
| RF-03 | Mantener cola cuando no hay capacidad inmediata | Alta | Prueba | TC-002 | tests/test_job_manager.py::test_cancel_queued_job (implica encolado) | PASS | Falta caso dedicado a medir la cola bajo saturación (ver RF-25) |
| RF-04 | Ejecutar en procesos separados sin bloquear nuevas solicitudes | Alta | Prueba | - | src/job_manager.py (subprocess.Popen por trabajo) + demo en src/main.py | PASS | - |
| RF-05 | Configurar y respetar máximo de trabajos simultáneos | Alta | Prueba | TC-002 | tests/test_job_manager.py::test_respects_concurrency_limit | PASS | - |
| RF-06 | Representar estados QUEUED/RUNNING/SUCCEEDED/FAILED/CANCELED | Alta | Prueba | TC-003 | tests/test_job_manager.py::test_job_reaches_succeeded_with_exit_code_zero, test_job_reaches_failed_with_nonzero_exit_code | PASS | - |
| RF-07 | Registrar tiempos de recepción/inicio/fin y código de salida | Alta | Prueba | TC-003, TC-006 | Campos submitted_at/started_at/finished_at/exit_code en Job (job_manager.py) | PASS | - |
| RF-08 | Consultar estado y metadatos de un trabajo por ID | Alta | Prueba | TC-004 | tests/test_job_manager.py::test_status_of_unknown_job_raises + demo | PASS | - |
| RF-09 | Listar trabajos con filtro básico por estado | Alta | Prueba | TC-004 | tests/test_job_manager.py::test_list_filters_by_state | PASS | - |
| RF-10 | Cancelar trabajo en cola o en ejecución | Alta | Prueba | TC-005 | tests/test_job_manager.py::test_cancel_queued_job, test_cancel_running_job | PASS | - |
| RF-11 | Capturar stdout y stderr sin mezclarlos | Alta | Prueba | TC-006 | tests/test_job_manager.py::test_stdout_and_stderr_are_captured_separately | PASS | - |
| RF-12 | Conservar metadatos y resultados tras reiniciar el servicio | Alta | Prueba | TC-007 | - | Pendiente | - |
| RF-13 | Recuperar historial persistido al arrancar | Alta | Prueba | TC-007 | - | Pendiente | - |
| RF-14 | Bitácora de eventos con marca temporal e ID de trabajo | Alta | Prueba | - | - | Pendiente | - |
| RF-15 | Inicio/cierre controlado, sin aceptar trabajos durante cierre | Media | Prueba | TC-009 | - | Pendiente | Método shutdown() existe pero falta atarlo a señal SIGTERM/SIGINT del propio servicio |
| RF-16 | Configurar directorio de datos, concurrencia, interfaz y puerto | Media | Inspección | TC-013 | - | Pendiente | Solo configurable por parámetros del constructor; falta CLI/archivo de configuración |
| RF-17 | Ayuda de uso y códigos de salida adecuados en el cliente | Media | Inspección | TC-015 | - | Pendiente | argparse da ayuda automática; faltan códigos de salida formalizados en todos los casos |
| RF-18 | Cliente remoto: enviar, consultar, listar, cancelar | Alta | Prueba | TC-010 | - | Pendiente | - |
| RF-19 | Operación local y remota con la misma semántica | Alta | Prueba | TC-010 | - | Pendiente | - |
| RF-20 | Restringir acceso remoto a redes/direcciones permitidas | Alta | Prueba | TC-011 | - | Pendiente | - |
| RF-21 | Protocolo con delimitación de mensajes y tolerancia a lecturas parciales | Alta | Prueba | TC-012 | - | Pendiente | - |
| RF-22 | Manejar desconexiones de cliente sin terminar el servicio | Alta | Prueba | TC-012, TC-019 | - | Pendiente | - |
| RF-23 | Rechazar y registrar solicitudes que excedan límites | Alta | Prueba | - | - | Pendiente | - |
| RF-24 | Resumen de salud del servicio | Alta | Prueba | TC-013 | - | Pendiente | - |
| RF-25 | Rechazo explícito al saturar la cola | Alta | Prueba | TC-016 | - | Pendiente | - |
| RF-26 | Cancelaciones concurrentes con estado final coherente | Alta | Prueba | TC-017 | - | Pendiente | - |
| RF-27 | Solicitud duplicada sin estados contradictorios | Alta | Prueba | TC-018 | - | Pendiente | - |
| RF-28 | Desconexión durante solicitud con estado coherente | Alta | Prueba | TC-019 | - | Pendiente | - |
| RF-29 | Detectar terminación inesperada de proceso hijo | Crítica | Prueba | TC-020 | tests/test_job_manager.py::test_nonexistent_binary_marks_job_failed_not_crash (caso parcial) | Pendiente | Cubre binario inexistente; falta caso de proceso que muere a medio camino (señal externa) |
| RF-30 | Política de escalamiento si no termina tras cancelación | Alta | Prueba | TC-021 | - | Pendiente | - |
| RNF-01 | Compilar/ejecutar en distribución Linux declarada | Alta | Inspección | TC-014 | Probado en Linux (sandbox) y Windows (dev); falta declarar formalmente la distro objetivo | Pendiente | - |
| RNF-02 | Construcción reproducible desde clon limpio | Alta | Inspección | TC-014 | verif/scripts/run_tests.sh existe | Pendiente | Falta documento de dependencias/versión fijada |
| RNF-03 | Sin privilegios root para operación normal | Alta | Inspección | TC-014 | El código no usa ninguna llamada que requiera privilegios elevados | PASS | - |
| RNF-04 | Al menos 3 trabajos simultáneos con límite=3 | Alta | Prueba | TC-002 | tests/test_job_manager.py::test_respects_concurrency_limit (probado con límite=2) | Pendiente | Falta TC-002 formal con límite=3 exacto |
| RNF-05 | Consulta de estado ≤1s con 100 trabajos | Alta | Prueba | TC-004 | - | Pendiente | - |
| RNF-06 | Soportar 500 registros sin pérdida de metadatos | Alta | Prueba | - | - | Pendiente | - |
| RNF-07 | Cola no inicia más procesos que el límite | Alta | Prueba | TC-002 | tests/test_job_manager.py::test_respects_concurrency_limit | PASS | - |
| RNF-08 | Solicitud inválida/desconexión no termina el servicio | Crítica | Prueba | TC-008 | tests/test_job_manager.py::test_submit_rejects_empty_command, test_nonexistent_binary_marks_job_failed_not_crash | PASS | - |
| RNF-09 | Terminación anormal no afecta a otros trabajos | Crítica | Prueba | TC-008 | tests/test_job_manager.py::test_nonexistent_binary_marks_job_failed_not_crash | PASS | - |
| RNF-10 | Tras reinicio no reportar RUNNING un proceso no controlado | Alta | Prueba | TC-007 | - | Pendiente | - |
| RNF-11 | Escrituras persistentes sin estado parcial | Alta | Prueba | TC-007 | - | Pendiente | - |
| RNF-12 | No escuchar en interfaces públicas por defecto | Alta | Prueba | TC-011 | - | Pendiente | - |
| RNF-13 | Acceso remoto limitado a localhost/LAN/VPN | Alta | Prueba | TC-011 | - | Pendiente | - |
| RNF-14 | Validar longitud y formato de mensajes de red | Alta | Prueba | TC-012 | - | Pendiente | - |
| RNF-15 | Registros no exponen secretos | Alta | Prueba | - | - | Pendiente | - |
| RNF-16 | Mínimo privilegio y modelo de amenazas básico | Alta | Prueba | - | - | Pendiente | - |
| RNF-17 | Código modular, sin archivos monolíticos injustificados | Alta | Prueba | - | - | Pendiente | - |
| RNF-18 | Interfaces públicas y decisiones documentadas | Alta | Prueba | - | - | Pendiente | - |
| RNF-19 | Compilar sin advertencias nuevas | Alta | Prueba | - | - | Pendiente | - |
| RNF-20 | Pruebas automatizadas con un único comando | Media | Inspección | - | verif/scripts/run_tests.sh corre todo con un solo comando | PASS | - |
| RNF-21 | Mensajes de error con causa y acción sugerida | Alta | Prueba | TC-015 | - | Pendiente | - |
| RNF-22 | Bitácora correlaciona solicitud con trabajo | Alta | Prueba | - | - | Pendiente | - |
| RNF-23 | Guía de usuario permite operar sin asistencia | Alta | Prueba | TC-015 | - | Pendiente | - |
| RNF-24 | Protocolo funciona con mensajes fragmentados | Alta | Prueba | TC-012 | - | Pendiente | - |
| RNF-25 | Liberar sockets y procesos hijo al cerrar | Alta | Prueba | TC-009 | - | Pendiente | - |
| RNF-26 | Demo remota solo en LAN/VPN, sin exposición a Internet | Alta | Prueba | TC-010 | - | Pendiente | - |
| RNF-27 | Transiciones de estado consistentes ante concurrencia | Crítica | Prueba | TC-017 | tests/test_job_manager.py::test_cancel_queued_job, test_cancel_running_job (cubren transición simple) | Pendiente | Falta caso de cancelaciones concurrentes duplicadas (RF-26 / TC-017) |
| RNF-28 | Actualizaciones persistentes atómicas o recuperables | Alta | Prueba | TC-022 | - | Pendiente | - |
| RNF-29 | Backpressure o rechazo explícito en los límites | Alta | Prueba | TC-016 | - | Pendiente | - |
| RNF-30 | Sin procesos huérfanos tras cierre o falla | Alta | Prueba | TC-020 | - | Pendiente | - |
| RNF-31 | Recuperación distingue pendientes/terminados/interrumpidos | Alta | Prueba | TC-022 | - | Pendiente | - |
| RNF-32 | Protocolo define compatibilidad de versión | Alta | Prueba | TC-023 | - | Pendiente | - |
| RNF-33 | Pruebas de estrés liberan memoria/procesos/sockets | Alta | Prueba | TC-024 | - | Pendiente | - |
| RNF-34 | Decisiones de seguridad/consistencia/recuperación con análisis de riesgo | Alta | Prueba | - | - | Pendiente | - |

## Notas

- La columna **Evidencia** para los ítems en PASS del Hito 1 apunta a
  pruebas unitarias concretas en `tests/test_job_manager.py`
  (12/12 en verde, ver `verif/scripts/run_tests.sh`), no todavía a casos
  TC-XXX documentados de forma independiente en `verif/test-cases/` — eso
  se completará junto con el resto del plan de verificación.
- Los ítems marcados **Pendiente** con evidencia parcial señalan qué falta
  exactamente en la columna Defecto/Excepción, para dar seguimiento claro.
- RNF relacionados con red y seguridad (RNF-12 a RNF-26 aprox.) están
  correctamente en Pendiente: corresponden al Hito 3 según doc. 06.
