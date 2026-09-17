<div align="center">

# ⚙️ Q-umplidor

### Gestor de trabajos para Linux — procesos, concurrencia y control en segundo plano

*Proyecto de **Qiskit Team** — Programación de Sistemas Avanzados 2026B*

![Status](https://img.shields.io/badge/estado-Hito%201%20en%20progreso-brightgreen)
![Lenguaje](https://img.shields.io/badge/lenguaje-Python%203-blue)
![Plataforma](https://img.shields.io/badge/plataforma-Linux-informational)
![Tests](https://img.shields.io/badge/pruebas-12%2F12%20PASS-success)
![Licencia](https://img.shields.io/badge/licencia-académica-lightgrey)

</div>

---

## 📑 Índice

- [Propósito](#-propósito)
- [Integrantes](#-integrantes)
- [Construcción provisional](#️-construcción-provisional)
- [Preparación y ejecución](#-preparación-y-ejecución)
- [Planeación](#-planeación)
- [Verificación prevista](#-verificación-prevista)
- [Estado del proyecto](#-estado-del-proyecto)
- [Documentación del repositorio](#-documentación-del-repositorio)

---

## 🎯 Propósito

**Q-umplidor** es un gestor de trabajos (*job runner*) para Linux capaz de **recibir, ejecutar, supervisar y administrar procesos** en segundo plano, con control de concurrencia, persistencia y acceso remoto restringido a red privada.

> El nombre juega con la idea de un sistema que **cumple** — cumple trabajos, cumple requisitos, cumple con lo prometido.

---

## 👥 Integrantes

| Nombre | Rol | Correo |
|---|---|---|
| Oscar Omar Aguilera De La Torre | 🧭 Responsable principal | oscar.aguilera7936@alumnos.udg.mx |
| Marlene Ximena Sandoval Garcia | 🛠️ Ingeniería | marlene.sandoval5114@alumnos.udg.mx |
| Ruy Eleazar Valle Rojas | ✅ Verificación | ruy.valle6299@alumnos.udg.mx |
| Diego Misael Camacho Nuño | 🔍 Revisor de producto | diego.camacho8526@alumnos.udg.mx |

📋 Matriz completa de responsables y revisores por área: [`project-management/roles.md`](project-management/roles.md)

---

## 🏗️ Construcción provisional

### Tecnologías y entorno

| | |
|---|---|
| 🐍 **Lenguaje** | Python 3 *(confirmado — ver [ADR-0001](docs/decisions/0001-lenguaje-runtime.md), estado: Aceptado)* |
| 🐧 **Sistema operativo objetivo** | Linux *(desarrollo también probado en Windows por portabilidad de las pruebas)* |
| 🧵 **Modelo de concurrencia** | Pool de hilos + cola compartida, ver [ADR-0002](docs/decisions/0002-modelo-concurrencia.md), estado: Aceptado |

### 🗂️ Estructura del proyecto

```text
Q-Core/
├── README.md                    # Visión, construcción, ejecución y prueba.
├── src/                         # Código de producción.
├── docs/
│   ├── user-guide/              # Instalación y operación.
│   ├── technical-guide/         # Arquitectura, protocolo, persistencia y decisiones.
│   ├── decisions/               # Decisiones de arquitectura — ADR.
│   ├── ai-usage/                # Registro del uso de IA.
│   ├── change-requests/         # Cambios del cliente y análisis de impacto.
│   └── incidents/               # Síntomas, evidencia, hipótesis, causa, corrección y regresión.
├── verif/
│   ├── verification-plan/       # Plan y matriz de trazabilidad.
│   ├── test-cases/              # Casos TC-XXX.
│   ├── scripts/                 # Automatización.
│   ├── test-data/               # Datos controlados.
│   └── results/                 # Evidencia por ejecución.
├── project-management/          # Planificación, roles, minutas, acuerdos y evidencia.
└── .github/
    └── ISSUE_TEMPLATE/          # Plantillas de trabajo y defectos.
```

---

## 🚀 Preparación y ejecución

**1. Clonar el repositorio**

```bash
git clone https://github.com/Maliboo127/Q-Core.git
cd Q-Core
```

**2. Correr las pruebas automatizadas**

```bash
python3 -m pip install pytest
python3 -m pytest tests/ -v
```

**3. Ver una demostración completa del flujo local**

```bash
python3 src/main.py demo
```

Esto envía varios trabajos, cancela uno en ejecución, lista todos los trabajos y muestra su estado y código de salida final — el flujo mínimo exigido para el Hito 1.

**4. Usar el cliente de línea de comandos**

```bash
python3 src/main.py submit -- echo "hola"
python3 src/main.py list
python3 src/main.py status <job_id>
python3 src/main.py cancel <job_id>
```

> ⚠️ **Limitación conocida:** cada invocación separada del CLI crea un gestor de trabajos nuevo (todavía no hay un servicio en segundo plano ni persistencia), así que `status`/`list` no ven trabajos enviados en una terminal distinta. Para ver el flujo completo en una sola ejecución, usa el modo `demo`. Esto se resuelve en el Hito 2. Detalle completo en [`docs/technical-guide/architecture.md`](docs/technical-guide/architecture.md).

---

## 🔹 Planeación

El proyecto se construye por etapas incrementales:

| Etapa | Qué agrega |
|---|---|
| **1️⃣ Núcleo local** | Ejecutar, consultar y cancelar trabajos de forma local. |
| **2️⃣ Concurrencia y persistencia** | Manejar varios trabajos a la vez, guardar resultados y recuperarse ante reinicio o falla. |
| **3️⃣ Acceso remoto** | Operar el sistema desde otros equipos dentro de una red privada o VPN. |

El código y la documentación se actualizan de forma incremental conforme se cierra cada etapa.

🗓️ Cronograma con fechas objetivo por hito: [`project-management/cronograma.md`](project-management/cronograma.md)
📌 Tablero de tareas y riesgos en vivo: [GitHub Projects — Cronograma Q-umplidor](https://github.com/users/Misaelcamacho89/projects/2/views/1)

---

## 🔸 Verificación prevista

A lo largo de las distintas etapas se realizarán pruebas para verificar que el sistema se comporta como se espera, tanto en condiciones normales como ante fallas o alta demanda.

Cada prueba y su resultado se documentarán como evidencia reproducible dentro del repositorio (`verif/results/`), permitiendo dar seguimiento al cumplimiento de los requisitos a lo largo del tiempo. Los defectos identificados se registrarán como Issues y se corregirán antes de avanzar a la siguiente etapa.

---

## 📊 Estado del proyecto

🟢 **Etapa actual: Hito 1 — Núcleo local (Avance 01)**

- [x] Roles del equipo definidos
- [x] Repositorio y estructura mínima creados
- [x] ADR-0001 (lenguaje) y ADR-0002 (concurrencia) — **Aceptados**, con prototipo funcional de evidencia
- [x] Cronograma y riesgos iniciales registrados
- [x] Núcleo local funcional: envío, ID único, ejecución como proceso separado, estados, consulta, listado, cancelación, código de salida
- [x] 12/12 pruebas unitarias automatizadas en verde
- [x] Arquitectura y modelo de estados documentados
- [x] Matriz de trazabilidad en construcción (64 requisitos, sin huecos)
- [x] Acceso del profesor confirmado como colaborador
- [ ] Persistencia entre reinicios (Hito 2)
- [ ] Acceso remoto vía LAN/VPN (Hito 3)

---

## 📚 Documentación del repositorio

| Recurso | Ubicación |
|---|---|
| 🧩 Decisiones de arquitectura (ADR) | [`docs/decisions/`](docs/decisions/) |
| 🏗️ Arquitectura del núcleo local | [`docs/technical-guide/architecture.md`](docs/technical-guide/architecture.md) |
| 🔄 Modelo de estados | [`docs/technical-guide/state-model.md`](docs/technical-guide/state-model.md) |
| 🤖 Registro de uso de IA | [`docs/ai-usage/`](docs/ai-usage/) |
| 🗓️ Cronograma | [`project-management/cronograma.md`](project-management/cronograma.md) |
| 👥 Roles y revisores | [`project-management/roles.md`](project-management/roles.md) |
| ✅ Matriz de trazabilidad | [`verif/verification-plan/traceability-matrix.md`](verif/verification-plan/traceability-matrix.md) |
| 📸 Evidencia de la demo (Avance 01) | [`verif/results/run-001-avance01/`](verif/results/run-001-avance01/) |
| 🐛 Plantillas de Issues | [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) |

---

<div align="center">

*Hecho con 🧠 y bastante café por Qiskit Team*

</div>
