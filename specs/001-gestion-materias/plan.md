# Implementation Plan: Gestión de Materias (HU-01)

**Branch**: `feature/HU-01-gestion-materias` | **Date**: 2026-09-16 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-gestion-materias/spec.md`

## Summary

Permitir crear, editar, listar y eliminar materias, validando nombre
obligatorio y único (sin distinguir mayúsculas/minúsculas), e impidiendo
eliminar una materia con tareas o exámenes asociados. Es la primera
historia implementada: sienta la estructura de carpetas (`domain/`,
`services/`, `repository/`, `ui/`) que van a reutilizar el resto de las
historias.

## Technical Context

**Language/Version**: Python 3.11+ (máquina de desarrollo tiene 3.14.7)

**Primary Dependencies**: Solo librería estándar (`sqlite3`, `tkinter`) para
código de producción. `pytest` y `pytest-bdd` como dependencias de
desarrollo/testing.

**Storage**: SQLite, archivo `cursada.db` en el directorio de datos de
usuario del SO (ver `research.md`). En esta historia se crea únicamente la
tabla `materias` — el resto del esquema se agrega incrementalmente en las
historias que lo necesiten (YAGNI).

**Testing**: `pytest` para dominio/servicios (TDD, ciclo RED/GREEN/REFACTOR),
`pytest-bdd` para el escenario de `features/gestion_materias.feature`.

**Target Platform**: Escritorio Linux y Windows.

**Project Type**: desktop-app, estructura de proyecto único (ver `CLAUDE.md`).

**Performance Goals**: Sin objetivos críticos — una operación CRUD sobre una
tabla de decenas de filas en SQLite local es instantánea en cualquier
hardware razonable.

**Constraints**: Debe funcionar sin conexión a internet. Sin frameworks de
UI pesados (ver `CLAUDE.md` → decisión de Tkinter sobre PySide/Electron/Tauri).

**Scale/Scope**: Un solo usuario por instalación; decenas de materias como
máximo.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Clean Code**: nombres de dominio en español, calcados de `CONTEXT.md`
  (`Materia`, `crear_materia`, `MateriaRepository`) — evita una capa de
  traducción entre el glosario y el código.
- ✅ **SOLID (SRP + DIP)**: un módulo de servicio por caso de uso
  (`crear_materia.py`, `editar_materia.py`, `eliminar_materia.py`,
  `listar_materias.py`); todos dependen de `MateriaRepository` (Protocol),
  no de `sqlite3` directo.
- ✅ **KISS**: sin ORM ni framework de migraciones — SQL directo con
  `sqlite3` stdlib y `CREATE TABLE IF NOT EXISTS`.
- ✅ **YAGNI**: solo la tabla `materias`; sin pantalla unificada todavía
  (esa es HU-16, historia aparte).
- ✅ **DRY**: la validación de formato (nombre no vacío) vive en la factory
  de dominio `crear_materia`; la de unicidad (requiere consultar datos)
  vive una sola vez en el service, no se duplica en la UI.
- ✅ **Repository / Factory function**: aplicados tal como los define la
  constitución — sin patrones nuevos no contemplados.

Sin violaciones. No aplica la sección de Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-gestion-materias/
├── plan.md              # este archivo
├── research.md          # Fase 0
├── data-model.md         # Fase 1
├── quickstart.md         # Fase 1
├── contracts/            # Fase 1
│   └── materia_repository.md
└── tasks.md              # Fase 2 (/speckit-tasks, todavía no generado)
```

### Source Code (repository root)

```text
asistente_facultad/
├── domain/
│   └── materia.py            # entidad Materia + factory crear_materia()
├── services/
│   ├── crear_materia.py
│   ├── editar_materia.py
│   ├── eliminar_materia.py
│   └── listar_materias.py
├── repository/
│   ├── materia_repository.py         # Protocol (puerto)
│   ├── sqlite_materia_repository.py  # adaptador SQLite
│   └── db.py                         # conexión + creación de tablas
├── ui/
│   └── ventana_materias.py
└── main.py                           # wiring de dependencias

tests/
├── domain/
│   └── test_materia.py
└── services/
    ├── test_crear_materia.py
    ├── test_editar_materia.py
    └── test_eliminar_materia.py

features/
├── gestion_materias.feature
└── steps/
    └── test_gestion_materias.py
```

**Structure Decision**: Proyecto único (no hay frontend/backend separados:
es una app de escritorio). Esta es la primera historia, así que crea el
esqueleto de carpetas completo que reutilizará el resto del backlog.

## Complexity Tracking

*Sin violaciones a justificar — tabla omitida.*
