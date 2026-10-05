

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


## CP-004 — Consultar el estado

- **Entrada:** `estado 1`, con el trabajo `sleep 200 &` activo.
- **Resultado esperado:** mostrar el comando, el estado y el tiempo transcurrido del trabajo con ID 1.
- **Resultado obtenido:** apareció `[1] sleep 200 & -> En ejecución (5s)`.

## CP-005 — Listar trabajos

- **Entrada:** `listar`, después de crear un trabajo con `sleep 200 &`.
- **Resultado esperado:** mostrar los trabajos registrados con su ID, estado, tiempo transcurrido y comando.
- **Resultado obtenido:** se mostró el trabajo con ID 1, estado «En ejecución», tiempo transcurrido de 20 segundos y comando `sleep 200 &`.

## CP-006 — Solicitar la cancelación

- **Entrada:** `cancelar 1`, con el trabajo `sleep 200 &` activo.
- **Resultado esperado:** detener el trabajo con ID 1 y permitir seguir escribiendo comandos.
- **Resultado obtenido:** apareció `Trabajo [1] cancelado`. Al consultar `estado 1`, el trabajo apareció como «Cancelado» y el programa continuó funcionando.

## CP-007 — Obtener el código de salida

- **Entrada:** `codigo 1`, después de que el trabajo con ID 1 termine correctamente.
- **Resultado esperado:** mostrar el código de salida 0.
- **Resultado obtenido:** apareció `codigo: el trabajo [1] terminó con código de salida 0`.

## CP-008 — Manejar un comando inválido

- **Entrada:** `hola`.
- **Resultado esperado:** indicar que no existe dicho programa
- **Resultado obtenido:** apareció `hola: comando no reconocido` y el programa continuó esperando comandos.
