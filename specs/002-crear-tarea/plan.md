# Implementation Plan: Crear Tarea Pendiente (HU-02)

**Branch**: `feature/HU-02-gestion-tareas` | **Date**: 2026-09-17 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-crear-tarea/spec.md`

## Summary

Permitir crear una tarea (materia, título, descripción opcional, fecha
límite, prioridad), validando título obligatorio, fecha no pasada y que la
materia exista, con estado inicial siempre "pendiente".

## Technical Context

**Language/Version**: Python 3.11+ (igual que HU-01).

**Primary Dependencies**: Solo librería estándar (`sqlite3`, `tkinter`,
`datetime`). Reutiliza `pytest`/`pytest-bdd` ya instalados.

**Storage**: SQLite (`cursada.db`, mismo archivo que HU-01). Se agregan las
tablas `estados`, `prioridades` (lookup, sembradas con valores fijos) y
`tareas` (extiende `eventos`, que ya existe desde HU-01).

**Testing**: `pytest` (dominio/servicios) + `pytest-bdd` (feature nuevo).

**Target Platform**: Escritorio Linux y Windows (sin cambios respecto a HU-01).

**Project Type**: desktop-app, mismo proyecto único que HU-01.

**Performance Goals / Constraints / Scale**: sin cambios respecto a HU-01.

## Constitution Check

- ✅ **Clean Code / SOLID / DIP**: `CrearTarea` depende de
  `TareaRepository` y `MateriaRepository` (ambos Protocol), no de SQLite.
- ✅ **KISS**: `Tarea` es un dataclass "plano" en el dominio — no se modela
  `Evento` como clase propia (ver `research.md`); el repositorio hace el
  join contra `eventos` por debajo.
- ✅ **YAGNI**: no se agrega edición/eliminación/cambio de estado de tareas
  acá — son HU-03 y HU-04, historias aparte.
- ✅ **DRY**: la validación de fecha no pasada vive una sola vez en la
  factory de dominio `crear_tarea`.
- ✅ **Repository / Factory function**: mismos patrones que HU-01, sin
  patrones nuevos.

Sin violaciones.

## Project Structure

### Documentation (this feature)

```text
specs/002-crear-tarea/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── tarea_repository.md
└── tasks.md
```

### Source Code (repository root)

```text
domain/
├── materia.py         # ya existe (HU-01)
└── tarea.py           # Tarea, EstadoTarea, PrioridadTarea, crear_tarea()

services/
├── crear_materia.py / editar_materia.py / eliminar_materia.py  # ya existen
└── crear_tarea.py     # depende de TareaRepository + MateriaRepository

repository/
├── db.py                          # se amplía: tablas estados/prioridades/tareas
├── materia_repository.py / sqlite_materia_repository.py  # ya existen
├── tarea_repository.py            # Protocol (puerto)
└── sqlite_tarea_repository.py     # adaptador SQLite

ui/
├── ventana_materias.py  # ya existe
└── ventana_tareas.py    # formulario de alta + listado simple de tareas

tests/
├── domain/test_tarea.py
├── services/test_crear_tarea.py
└── repository/test_sqlite_tarea_repository.py

features/
├── crear_tarea.feature
└── steps/test_crear_tarea.py
```

**Structure Decision**: se extiende el mismo proyecto único de HU-01, sin
carpetas nuevas de alto nivel.

## Complexity Tracking

*Sin violaciones a justificar.*
