# Research: Cambiar Estado de una Tarea (HU-04)

## Reutilizar `actualizar()` en vez de un método de repositorio nuevo

- **Decisión**: `CambiarEstadoTarea` obtiene la tarea actual
  (`TareaRepository.obtener`), construye la versión con el nuevo estado vía
  `cambiar_estado_tarea()` (dominio), y la persiste con
  `TareaRepository.actualizar()` — el mismo método que ya usa `EditarTarea`
  desde HU-03.
- **Rationale**: `actualizar()` ya hace `UPDATE` de todos los campos de
  `tareas` (incluido `estado_id`), así que no hace falta un método
  `cambiar_estado(id, estado)` dedicado en el repositorio — sería
  duplicar SQL que ya existe (DRY/YAGNI).

## `cambiar_estado_tarea()` como función de dominio, no solo un setter

- **Decisión**: se agrega una función pura en `domain/tarea.py`, con la
  misma forma que `editar_tarea()` (recibe la tarea actual, devuelve una
  `Tarea` nueva con el campo cambiado).
- **Rationale**: mantiene el criterio ya establecido de que toda
  transformación de una `Tarea` pasa por una función de dominio, no por
  mutación directa desde el service o la UI — aunque acá no haya ninguna
  regla de validación que proteger, es consistente con cómo está armado el
  resto del dominio y deja un único lugar si en el futuro apareciera una
  regla (por ejemplo, side-effects al completar una tarea).
