# Research: Editar/Eliminar Tarea (HU-03)

## Validación de fecha límite: solo si cambia

- **Decisión**: `editar_tarea(tarea_actual, ...)` recibe la tarea actual y
  compara la nueva `fecha_limite` contra `tarea_actual.fecha_limite`. Solo
  valida "no pasada" si son distintas.
- **Rationale**: es exactamente el mismo criterio que "editar sin cambiar
  el nombre" en `EditarMateria` (HU-01) — una operación que no modifica el
  campo conflictivo no debería fallar por una regla pensada para cuando sí
  cambia. Sin esto, cualquier tarea vencida quedaría "congelada": ni
  siquiera se podría corregirle la descripción sin antes empujarle la
  fecha a futuro.
- **Alternativas consideradas**: validar siempre contra `date.today()` sin
  importar si cambió — descartada por el problema de UX de arriba.

## Reutilizar la validación de título entre crear y editar

- **Decisión**: se extrae una función interna `_validar_titulo(titulo) ->
  str` (devuelve el título limpio o lanza `ValueError`), usada tanto por
  `crear_tarea` como por `editar_tarea`.
- **Rationale**: DRY — ya estaba duplicándose el `if not titulo.strip():
  raise ValueError(...)`.

## Eliminar una tarea: borrado real, en cascada a `eventos`

- **Decisión**: `SqliteTareaRepository.eliminar(id)` borra la fila de
  `tareas` y la de `eventos` en la misma operación (no hay "soft delete").
- **Rationale**: `tareas.evento_id` es la fila que le da sentido a la
  tarea — dejar el evento huérfano sin su fila en `tareas` rompería el
  join que usa `listar()`. FR-007 pide explícitamente que no quede rastro.
- **Alternativas consideradas**: soft delete con columna `eliminado` —
  descartado por YAGNI, no hay ningún requisito de recuperar tareas
  borradas ni de auditoría.

## Reasignar materia: mismo repositorio, sin repetir la regla

- **Decisión**: `EditarTarea` recibe también `MateriaRepository` (igual que
  `CrearTarea`) y valida existencia antes de guardar.
- **Rationale**: mismo criterio ya aplicado, sin necesidad de research
  adicional.
