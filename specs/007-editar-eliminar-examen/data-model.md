# Data Model: Editar/Eliminar Examen (HU-07)

Sin cambios de esquema. Operaciones nuevas sobre filas existentes:

- **Editar**: `UPDATE eventos SET materia_id=?, titulo=?, fecha=?, hora=?
  WHERE id=?` + `UPDATE examenes SET modalidad_id=?, notas=? WHERE
  evento_id=?`.
- **Eliminar**: `DELETE FROM examenes WHERE evento_id=?` + `DELETE FROM
  eventos WHERE id=?`.

## Reglas de validación (repetidas de `spec.md`)

- `tema` obligatorio → domain (`editar_examen`).
- `fecha` no puede ser pasada **solo si cambia** → domain (`editar_examen`).
- `hora` y `modalidad` obligatorias (siempre, no solo si cambian) → domain.
- `materia_id` debe existir → service (`EditarExamen`).
