# Implementation Plan: Cambiar Estado de una Tarea (HU-04)

**Branch**: `feature/HU-04-cambiar-estado-tarea` | **Date**: 2026-09-17 | **Spec**: [spec.md](./spec.md)

## Summary

Agregar la operación de cambiar el `estado` de una tarea existente a
cualquiera de los 3 valores, sin restricciones de transición.

## Technical Context

Sin cambios respecto a HU-03 (mismo stack, mismo `cursada.db`, sin cambios
de esquema).

## Constitution Check

- ✅ **DRY**: se reutiliza `TareaRepository.actualizar()` (ya existe desde
  HU-03) — no se agrega ningún método nuevo al contrato ni a la tabla.
- ✅ **KISS**: sin máquina de estados ni validación de transiciones (ver
  spec.md).
- ✅ **Factory function**: `cambiar_estado_tarea()` sigue el mismo patrón
  que `editar_tarea()` (devuelve una `Tarea` nueva, no muta in-place),
  consistente con el resto del dominio.

Sin violaciones. No se genera `contracts/` en esta historia: no hay ningún
método nuevo de repositorio que documentar como puerto.

## Project Structure

```text
domain/tarea.py                          # + cambiar_estado_tarea()
services/cambiar_estado_tarea.py         # nuevo
ui/ventana_tareas.py                     # + combo de estado + botón
tests/domain/test_tarea.py               # + tests de cambiar_estado_tarea
tests/services/test_cambiar_estado_tarea.py  # nuevo
features/cambiar_estado_tarea.feature    # nuevo
```

**Structure Decision**: mismo proyecto único, sin carpetas nuevas ni
cambios de esquema.

## Complexity Tracking

*Sin violaciones.*
