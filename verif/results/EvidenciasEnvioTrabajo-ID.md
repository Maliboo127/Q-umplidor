# Evidencia de verificación: versión 01 - Envío de trabajo (Sleep) y obtención de un ID (identificador único)

## 1. Identificación de la versión

| Campo | Valor |
|---|---|
| *Producto* | Enviar un trabajo (sleep) y obtener un identificador unico |
| *Versión* | Versión 01 (Avance 01) |
| *Commit evaluado* | 0177489, c99ad60, 4acabba, 5ca67f6, 66c4153|
| *Fecha de la demostración* | 02/10/2026 |
| *Responsable de la ejecución* | Diego Misael, Marlene, Ruy  |
| *Revisor* | Marlene, Ruy, Diego Misael |

## 2. Entorno de ejecución

| Campo | Valor |
|---|---|
| Sistema operativo | `Linux` |
| Versión de Python | `Python3`  |
| Comando de arranque | `python3 src/main.py` |

## 3. Alcance de la demostración

**Funcionalidades incluidas en esta versión:**

* Envío de un trabajo sleep N desde la consola Q-umplidor>.
* Asignación de un identificador único al trabajo enviado.

**Funcionalidades no incluidas en esta versión:**

* Consulta del estado de un trabajo.
* Listado de trabajos.
* Cancelación de trabajos.

### TC-001: Arranque de la consola

| Campo | Contenido |
|---|---|
| **Objetivo** | Verificar que el programa inicia y muestra el prompt `Q-umplidor>` |
| **Precondiciones** | Python instalado; terminal abierta en la raíz del repositorio |
| **Pasos** | 1. Ejecutar `python3 src/main.py`. |
| **Resultado esperado** | El arranque y la impresión del prompt `Q-umplidor>` |
| **Resultado obtenido** | Inicio del programa y muestra del prompt |
| **Estado** |✅ Aprobado |

![TC-001: arranque de la consola](img/TC-001.png)

### TC-002: Ejecución de `sleep N` en primer plano

| Campo | Contenido |
|---|---|
| **Objetivo** | Verificar que `sleep 10` ocupa la consola durante 10 segundos y luego devuelve el prompt |
| **Precondiciones** | Consola iniciada |
| **Pasos** | 1. Escribir `sleep [10]`. 2. Esperar a que termine. |
| **Resultado esperado** | Envió de `sleep 10` y que al terminar retorne el promt |
| **Resultado obtenido** | Se envía el `sleep 10` y al pasar el tiempo imprime el promt |
| **Estado** | ✅ Aprobado  |

![TC-002: sleep en primer plano](img/TC-002.png)
![TC-002: sleep en primer plano](img/TC-002.1.png)

### TC-003: Ejecución de `sleep N &` en segundo plano

| Campo | Contenido |
|---|---|
| **Objetivo** | Verificar que `sleep N &` crea un trabajo en segundo plano, devuelve un ID y libera el prompt de inmediato |
| **Precondiciones** | Consola iniciada; sin trabajos activos |
| **Pasos** | 1. Escribir `sleep [N] &`. 2. Observar la respuesta. |
| **Resultado esperado** | Enviar un trabajo, devuelve un ID y la liberación del promt |
| **Resultado obtenido** | La consola mostró ID = 1 y volvió a mostrar Q-umplidor> sin esperar los 10 segundos  |
| **Estado** | ✅ Aprobado  |

![TC-003: sleep en segundo plano](img/TC-003.png)


## 4. Resumen de resultados

| ID | Caso | Estado |
|---|---|---|
| TC-001 | Arranque de la consola | ✅ Aprobado |
| TC-002 | `sleep N`  | ✅ Aprobado |
| TC-003 | `sleep N &`  | ✅ Aprobado |


**Total:** 3️⃣ de 3️⃣ casos aprobados.

## 5. Defectos y limitaciones conocidos

| ID | Descripción | Caso relacionado | Estado |
|---|---|---|---|
| TC-001 |Sin defectos conocidos| - | - |
| TC-002 |Sin defectos conocidos| - | - |
| TC-003 |Sin defectos conocidos| - | - |


## 6. Conclusión
En esta primer versión queda demostrado que la consola arranca de forma exitosa, permitiendo el envió de trabajos, obtener un identificador único y la liberación del promt de forma inmediata. 

