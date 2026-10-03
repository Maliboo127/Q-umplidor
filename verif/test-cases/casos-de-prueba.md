

## CP-001 — Enviar un trabajo

- **Entrada:** `sleep 5`.
- **Resultado esperado:** aceptar el trabajo y correrlo en primer plano donde no deberia dejar ejecutar otro comando
- **Resultado obtenido** exactamente como el esperado

## CP-002 — Obtener un identificador único

- **Entrada:** escribir `sleep 200 &` 2 veces
- **Resultado esperado:** recibir un identificador diferente para cada trabajo.
- **Resultado obtenido:** aparece `ID: [1]` para el primero e `ID: [2]` para el segundo. La numeración es única dentro de la sesión; vuelve a comenzar al reiniciar.


## CP-003 — Ejecutar el trabajo como proceso separado


- **Entrada:** `sleep 200 &`.
- **Resultado esperado:** debe correr el trabajo permitiendo escribir nuevos comandos 
- **Resultado obtenido:** efectivamente despues de colocar el comando da una salida de ID y permite seguir escribiendo comandos  

<a id="tc-004"></a>
## TC-004 — Consultar el estado

- **Preparación:** tener activo un trabajo creado con `sleep 200 &`.
- **Entrada:** `listar`.
- **Resultado esperado:** poder consultar el estado del trabajo.
- **Resultado obtenido, confirmado por el usuario:** el trabajo aparece con el estado «En ejecución». La consulta actual se hace mediante el listado; no existe un comando individual `estado <id>`.

<a id="tc-005"></a>
## TC-005 — Listar trabajos

- **Preparación:** tener registrado el trabajo creado con `sleep 200 &`.
- **Entrada:** `listar`.
- **Resultado esperado:** mostrar los trabajos registrados con sus datos.
- **Resultado obtenido, confirmado por el usuario:** se mostró el trabajo con ID 1, estado «En ejecución», tiempo transcurrido y comando `sleep 200 &`.

<a id="tc-006"></a>
## TC-006 — Solicitar la cancelación

- **Preparación:** tener activo un trabajo con ID 1.
- **Entrada de prueba propuesta:** `cancelar 1`.
- **Resultado esperado del requisito:** detener el trabajo seleccionado y permitir que el programa siga atendiendo comandos.
- **Resultado actual:** aparece `cancelar: comando no reconocido`. La operación no está implementada y el trabajo no se cancela. El rechazo del comando se observó en la comprobación exploratoria anterior; no se ha realizado una nueva prueba sobre un trabajo activo.

<a id="tc-007"></a>
## TC-007 — Obtener el código de salida

- **Preparación:** esperar a que termine correctamente el trabajo con ID 1.
- **Entrada:** `codigo 1`.
- **Resultado esperado:** mostrar el código de salida 0 para una terminación correcta.
- **Resultado obtenido, confirmado por el usuario:** apareció `codigo: el trabajo [1] terminó con código de salida 0`.

## CP-008 — Manejar un comando inválido

- **Entrada:** `hola`.
- **Resultado esperado:** indicar que no existe dicho programa
- **Resultado obtenido:** apareció `hola: comando no reconocido` y el programa continuó esperando comandos.
