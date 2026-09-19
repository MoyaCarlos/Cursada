# Data Model: Ventana Principal con Vista Unificada (HU-16)

Sin cambios de esquema SQLite. Se agrega un tipo de solo lectura en la
capa de servicios (no persistido):

## ItemPendiente (servicio, no dominio)

| Campo            | Tipo             | Origen                                    |
|------------------|------------------|--------------------------------------------|
| `tipo`           | `"tarea"` \| `"examen"` | fijo según de cuál repositorio vino. |
| `id`             | int              | `Tarea.id` o `Examen.id`.                  |
| `materia_nombre` | str              | resuelto contra `MateriaRepository.listar()`. |
| `titulo`         | str              | `Tarea.titulo` o `Examen.tema`.            |
| `fecha`          | date             | `Tarea.fecha_limite` o `Examen.fecha`.     |
| `hora`           | time \| None     | `None` para tareas, `Examen.hora` para exámenes. |
| `estado`         | str \| None      | `Tarea.estado.value`, `None` para exámenes. |

Ordenado por `(fecha, hora o time.min)` ascendente.
