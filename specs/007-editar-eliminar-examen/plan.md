# Implementation Plan: Editar/Eliminar Examen (HU-07)

**Branch**: `feature/HU-07-editar-eliminar-examen` | **Date**: 2026-09-17 | **Spec**: [spec.md](./spec.md)

## Summary

Agregar edición y borrado de exámenes existentes, espejo de HU-03
(tareas): la fecha solo se valida como "no pasada" cuando cambia; hora y
modalidad siguen siendo obligatorias también al editar.

## Technical Context

Sin cambios de stack respecto a HU-06.

## Constitution Check

- ✅ **DRY**: se extrae `_validar_tema()` (paralelo a `_validar_titulo()`
  de tareas), reutilizada por `crear_examen` y `editar_examen`.
- ✅ **KISS**: sin restricción para eliminar (igual que tareas).
- ✅ **Repository**: se extiende `ExamenRepository` con
  `obtener`/`actualizar`/`eliminar`, mismo patrón que `TareaRepository`.

Sin violaciones.

## Project Structure

```text
specs/007-editar-eliminar-examen/
├── plan.md / research.md / data-model.md / quickstart.md
├── contracts/examen_repository.md   # actualiza el de HU-06
└── tasks.md

domain/examen.py                          # + editar_examen()
repository/examen_repository.py           # + obtener, actualizar, eliminar
repository/sqlite_examen_repository.py    # + implementación
services/editar_examen.py                 # nuevo
services/eliminar_examen.py               # nuevo
ui/ventana_examenes.py                    # + selección, editar, eliminar
tests/domain/test_examen.py               # + tests de editar_examen
tests/services/test_editar_examen.py      # nuevo
tests/services/test_eliminar_examen.py    # nuevo
tests/fakes.py                            # + obtener/actualizar/eliminar en ExamenRepositoryFake
features/editar_eliminar_examen.feature   # nuevo
```

**Structure Decision**: mismo proyecto único.

## Complexity Tracking

*Sin violaciones.*
