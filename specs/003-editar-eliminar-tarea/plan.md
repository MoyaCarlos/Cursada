# Implementation Plan: Editar/Eliminar Tarea (HU-03)

**Branch**: `feature/HU-03-editar-eliminar-tarea` | **Date**: 2026-09-17 | **Spec**: [spec.md](./spec.md)

## Summary

Agregar edición (título, descripción, fecha límite, prioridad, materia) y
borrado de tareas existentes, con la regla especial de que la fecha límite
solo se valida como "no pasada" cuando efectivamente cambia.

## Technical Context

Sin cambios respecto a HU-02 (mismo stack, mismo `cursada.db`).

## Constitution Check

- ✅ **DRY**: la validación de título vive en una sola función de dominio
  reutilizada por crear y editar (ver `research.md`).
- ✅ **KISS**: no se agrega historial de cambios ni "soft delete" — eliminar
  borra de verdad (FR-007), sin necesidad hoy de recuperar tareas borradas.
- ✅ **YAGNI**: no se toca el estado de la tarea acá (HU-04, aparte).
- ✅ **Repository**: se extiende `TareaRepository` con `obtener`,
  `actualizar`, `eliminar` — mismo patrón que `MateriaRepository`.

Sin violaciones.

## Project Structure

### Documentation (this feature)

```text
specs/003-editar-eliminar-tarea/
├── plan.md / research.md / data-model.md / quickstart.md
├── contracts/tarea_repository.md   # actualiza el contrato de HU-02
└── tasks.md
```

### Source Code

```text
domain/tarea.py            # + editar_tarea()
repository/tarea_repository.py         # + obtener, actualizar, eliminar
repository/sqlite_tarea_repository.py  # + implementación de esos 3 métodos
services/editar_tarea.py               # nuevo
services/eliminar_tarea.py             # nuevo
ui/ventana_tareas.py                   # + selección de tarea, botones Editar/Eliminar
tests/domain/test_tarea.py             # + tests de editar_tarea
tests/services/test_editar_tarea.py    # nuevo
tests/services/test_eliminar_tarea.py  # nuevo
tests/fakes.py                         # + obtener/actualizar/eliminar en TareaRepositoryFake
features/editar_eliminar_tarea.feature # nuevo
```

**Structure Decision**: mismo proyecto único, sin carpetas nuevas.

## Complexity Tracking

*Sin violaciones.*
