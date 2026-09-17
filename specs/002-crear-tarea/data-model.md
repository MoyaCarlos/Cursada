# Data Model: Crear Tarea Pendiente (HU-02)

## Tarea (dominio)

| Campo          | Tipo            | Reglas                                                    |
|----------------|-----------------|-------------------------------------------------------------|
| `id`           | int \| None     | Id del `evento` asociado (autoincremental, ver abajo).       |
| `materia_id`   | int             | Obligatorio. Debe referenciar una materia existente.         |
| `titulo`       | str             | Obligatorio. No vacío ni solo espacios.                      |
| `descripcion`  | str             | Opcional (default `""`).                                     |
| `fecha_limite` | date            | Obligatorio. No puede ser anterior a hoy.                    |
| `prioridad`    | PrioridadTarea  | Default `MEDIA`. Valores: `BAJA`, `MEDIA`, `ALTA`.           |
| `estado`       | EstadoTarea     | Siempre `PENDIENTE` al crear (cambiarlo es HU-04).           |

## Tablas SQLite creadas en esta historia

```sql
CREATE TABLE IF NOT EXISTS estados (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);
INSERT OR IGNORE INTO estados (id, nombre) VALUES
    (1, 'pendiente'), (2, 'en_progreso'), (3, 'completada');

CREATE TABLE IF NOT EXISTS prioridades (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);
INSERT OR IGNORE INTO prioridades (id, nombre) VALUES
    (1, 'baja'), (2, 'media'), (3, 'alta');

CREATE TABLE IF NOT EXISTS tareas (
    evento_id INTEGER PRIMARY KEY REFERENCES eventos(id),
    descripcion TEXT NOT NULL DEFAULT '',
    estado_id INTEGER NOT NULL REFERENCES estados(id),
    prioridad_id INTEGER NOT NULL REFERENCES prioridades(id)
);
```

`tareas.evento_id` es a la vez PK y FK: cada tarea *es* un evento (relación
1 a 1 de "extensión", ver `docs/modelo-datos.md`). Crear una tarea implica
insertar primero en `eventos` (materia_id, titulo, fecha) y después en
`tareas` (con el mismo id), dentro de una sola operación del repositorio.

## Reglas de validación (repetidas de `spec.md`)

- `titulo` obligatorio, no vacío ni solo espacios → domain (`crear_tarea`).
- `fecha_limite` no puede ser anterior a hoy → domain (`crear_tarea`).
- `materia_id` debe existir → service (`CrearTarea`, vía `MateriaRepository`).
- `prioridad` default `MEDIA` si no se especifica → domain (`crear_tarea`).
- `estado` siempre `PENDIENTE` al crear → domain (`crear_tarea`, no es un
  parámetro del constructor).
