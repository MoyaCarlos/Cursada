# Data Model: Editar/Eliminar Tarea (HU-03)

Sin cambios al esquema de tablas (ver `docs/modelo-datos.md` y
`specs/002-crear-tarea/data-model.md`). Esta historia solo agrega
operaciones sobre las filas ya existentes:

- **Editar**: `UPDATE eventos SET materia_id=?, titulo=?, fecha=? WHERE
  id=?` + `UPDATE tareas SET descripcion=?, estado_id=?, prioridad_id=?
  WHERE evento_id=?` (dos tablas, misma transacción lógica).
- **Eliminar**: `DELETE FROM tareas WHERE evento_id=?` + `DELETE FROM
  eventos WHERE id=?` (en ese orden, por la FK).

## Reglas de validación (repetidas de `spec.md`)

- `titulo` obligatorio → domain (`editar_tarea`, misma regla que `crear_tarea`).
- `fecha_limite` no puede ser pasada **solo si cambia** → domain
  (`editar_tarea`, comparando contra la tarea actual).
- `materia_id` debe existir → service (`EditarTarea`, vía `MateriaRepository`).
