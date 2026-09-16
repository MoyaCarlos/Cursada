<!--
Sync Impact Report
- Version change: (template) → 1.0.0
- Modified principles: n/a (initial ratification)
- Added sections: Core Principles (I–V), Arquitectura y Patrones de Diseño,
  Proceso de Desarrollo, Governance
- Removed sections: n/a
- Follow-up TODOs: none — todos los valores se derivaron de CLAUDE.md, que ya
  documenta las decisiones de arquitectura, proceso y stack del proyecto.
-->
# Cursada Constitution

## Core Principles

### I. Clean Code
Nombres claros que expliquen intención, funciones pequeñas con una sola
responsabilidad. No se escriben comentarios que expliquen el "qué" del código
(eso ya lo dicen los nombres); solo se documenta el "por qué" cuando no es
obvio (una restricción oculta, un workaround puntual).

### II. SOLID (SRP y Dependency Inversion)
Cada `service` implementa un único caso de uso (Single Responsibility). Los
`services` dependen de interfaces de repositorio (`Protocol`), nunca de
`sqlite3` concreto ni de detalles de infraestructura. La dirección de
dependencia siempre apunta hacia `domain/`: el dominio no conoce SQLite,
Tkinter ni cómo se envía un email.

### III. KISS
Se prefiere siempre la solución más simple que cumpla el requerimiento sobre
una más sofisticada. Ejemplos ya decididos bajo este criterio: el motor de
recordatorios usa polling periódico en vez de un mecanismo en tiempo real; el
filtro por estado (pendiente/completado) se resuelve en memoria (Python) en
vez de con SQL complejo, dado el volumen chico de datos de una app personal.

### IV. YAGNI
No se construyen abstracciones ni funcionalidades para necesidades
hipotéticas. Quedan explícitamente fuera de alcance mientras no se demuestren
necesarias: sincronización de datos entre dispositivos, canal de
notificación por Telegram, y estado explícito de "rendido" en exámenes (se
infiere por fecha en vez de agregar una columna).

### V. DRY
Toda regla de negocio vive en un único lugar dentro de `domain/` — por
ejemplo, el cálculo de cuándo corresponde disparar un recordatorio, o la
regla de qué cuenta como "completado" para cada tipo de evento. Ninguna
regla de negocio se duplica entre `repository/`, `services/` y `ui/`.

## Arquitectura y Patrones de Diseño

Arquitectura Clean/Hexagonal liviana (Ports & Adapters), sin más capas que
las necesarias:

```
domain/          -> entidades y reglas de negocio
services/        -> casos de uso
repository/      -> interfaces de persistencia + implementación SQLite
notifications/   -> adaptadores por canal de notificación
ui/              -> Tkinter + pystray
```

Patrones aplicados:
- **Repository**: abstrae la persistencia detrás de interfaces, habilita
  tests con fakes en memoria sin tocar disco.
- **Strategy**: cada canal de notificación (email, escritorio, y Telegram a
  futuro) implementa una interfaz común `Notificador.enviar(mensaje)`.
- **Factory function**: constructores (`crear_tarea`, `crear_examen`) que
  validan invariantes de dominio al momento de crear la entidad.

Cualquier desviación de esta estructura (una capa nueva, una dependencia que
cruce hacia adentro) debe justificarse explícitamente en la spec de la
historia correspondiente.

## Proceso de Desarrollo

Proyecto individual: sin roles de equipo, sin aprobación de otro integrante
en PR (el autor revisa su propio diff antes de mergear).

- **SDD**: GitHub Spec Kit. Flujo por historia: `/speckit-constitution` (una
  vez) → `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` →
  `/speckit-tasks` → `/speckit-implement`. Specs versionadas en
  `specs/<feature>/`, con reglas de negocio, casos límite y errores en
  formato EARS. `/speckit-implement` se corre una historia a la vez, con
  revisión del diff antes de continuar.
- **BDD**: `pytest-bdd`. Escenarios Gherkin en `/features`, cubriendo casos
  normales, alternativos, límite y de error.
- **TDD**: `pytest`, foco en `domain/` y `services/`. Ciclo RED → GREEN →
  REFACTOR, evidenciado en commits separados (`RED: ...`, `GREEN: ...`,
  `REFACTOR: ...`). No se fuerza un commit de REFACTOR vacío. No aplica a
  código trivial (getters, DTOs).
- **Git**: rama por historia (`feature/HU-XX-nombre-corto`). Merge a `main`
  siempre con "Create a merge commit" (nunca squash), para conservar en el
  historial la evidencia del ciclo RED/GREEN/REFACTOR.
- **Definition of Done**: código mergeado a `main`; test unitario (TDD) y
  escenario BDD correspondiente, ambos en verde; spec SDD escrita en
  `specs/`; sin defectos abiertos bloqueantes para esa historia.

## Governance

Esta constitución tiene prioridad sobre cualquier otra práctica o preferencia
puntual durante el desarrollo. Todo plan (`/speckit-plan`) y toda tarea
(`/speckit-tasks`) deben verificar cumplimiento de estos principios antes de
avanzar a `/speckit-implement`; cualquier complejidad que se aparte de ellos
debe quedar justificada por escrito en la spec de la historia.

Las enmiendas a esta constitución se hacen editando este archivo, incrementando
`CONSTITUTION_VERSION` según versionado semántico (MAYOR: eliminación o
redefinición incompatible de un principio; MENOR: principio o sección nueva;
PARCHE: aclaraciones o correcciones de redacción) y actualizando
`LAST_AMENDED_DATE`. El detalle de stack tecnológico, modelo de datos y
backlog vive en `CLAUDE.md` y `docs/`, que esta constitución no reemplaza.

**Version**: 1.0.0 | **Ratified**: 2026-09-16 | **Last Amended**: 2026-09-16
