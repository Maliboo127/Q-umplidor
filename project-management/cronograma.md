# Cronograma inicial — Q-umplidor

Fechas objetivo por hito, alineadas con "06 — JobRunner — Hitos y Revisiones
Técnicas". Se ajustarán conforme el profesor confirme fechas oficiales de cada
entrega; mientras tanto sirven como línea base de planeación interna.

| Hito / Entrega | Objetivo | Fecha objetivo | Responsable de cierre |
|---|---|---|---|
| Avance 0 | Formación de equipo y repositorio | Hoy | Oscar (responsable principal) |
| Hito 1 — Núcleo local | Envío local, ID, proceso hijo, estados básicos, stdout/stderr, cola inicial | +2 semanas | Marlene (ingeniería) |
| RT-1 | Revisión técnica: diseño de procesos, señales, calidad del repo | Junto con cierre de Hito 1 | Ruy (verificación) |
| Avance 1 | Primer entregable formal de producto | Según fecha del curso | Oscar |
| Hito 2 — Concurrencia y persistencia | Límite de concurrencia, cola estable, cancelación, persistencia, recuperación, bitácora | +2 semanas tras Hito 1 | Marlene |
| RT-2 | Revisión técnica: condiciones de carrera, formato persistente, pruebas de integración | Junto con cierre de Hito 2 | Ruy |
| Hito 3 — Operación remota privada | Protocolo documentado, cliente remoto, restricción LAN/VPN | +2 semanas tras Hito 2 | Marlene |
| RT-3 | Revisión técnica: framing, superficie de ataque, bind y reglas de acceso | Junto con cierre de Hito 3 | Ruy |
| Hito 4 — Candidato de entrega | Documentación completa, matriz sin huecos, verificación cruzada con otro equipo | +1-2 semanas tras Hito 3 | Diego (revisor de producto) |
| Hito 5 — Aceptación final | Versión etiquetada, release notes, defensa individual | Fecha de entrega final del curso | Todo el equipo |

## Notas
- Las fechas exactas de Avance 1, RT-1/2/3 y entrega final deben confirmarse
  contra el calendario oficial publicado por el profesor y actualizarse aquí.
- Cada cierre de hito requiere, además del código, documentación, trazabilidad,
  registro de uso de IA y evidencia (ver Definición de terminado, doc. 04).

## Riesgos y dependencias conocidos
Registrados como Issues en el tablero del proyecto (#94–#99):
- Depender de una sola persona para integrar, probar y entregar el trabajo.
- Que un integrante se atrase y no lo comunique a tiempo.
- No poder explicar por qué se tomó una decisión importante (riesgo de defensa
  individual, doc. 05 y 06).
- Que otras materias o compromisos reduzcan el tiempo disponible antes de una
  entrega.
- Seguir trabajando sobre una interpretación incorrecta por no preguntar a tiempo
  (dudas de alcance deben consultarse antes de asumir, doc. Project Brief).
- Evitar señalar problemas para no generar desacuerdos dentro del equipo.

## Dependencia externa
- Acceso a una segunda máquina/red LAN o VPN es necesario antes del Hito 3 y su
  demostración (RF-18–RF-22, RNF-26); debe coordinarse con anticipación.
- Verificación cruzada con otro equipo (Hito 4) depende de que ambos equipos
  lleguen a esa etapa en fechas compatibles.
