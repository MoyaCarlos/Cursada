# Data Model: Crear Examen (HU-06)

## Examen (dominio)

| Campo        | Tipo             | Reglas                                              |
|--------------|------------------|-------------------------------------------------------|
| `id`         | int \| None      | Id del `evento` asociado.                             |
| `materia_id` | int              | Obligatorio. Debe referenciar una materia existente.  |
| `tema`       | str              | Obligatorio. No vacío ni solo espacios.               |
| `fecha`      | date             | Obligatorio. No puede ser anterior a hoy.             |
| `hora`       | time             | Obligatorio (a diferencia de la fecha límite de una Tarea). |
| `modalidad`  | ModalidadExamen  | Obligatorio. Sin default (`PRESENCIAL`/`VIRTUAL`).    |
| `notas`      | str              | Opcional (default `""`).                              |

## Tablas SQLite creadas en esta historia

```sql
CREATE TABLE IF NOT EXISTS modalidades (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);
INSERT OR IGNORE INTO modalidades (id, nombre) VALUES
    (1, 'presencial'), (2, 'virtual');

CREATE TABLE IF NOT EXISTS examenes (
    evento_id INTEGER PRIMARY KEY REFERENCES eventos(id),
    modalidad_id INTEGER NOT NULL REFERENCES modalidades(id),
    notas TEXT NOT NULL DEFAULT ''
);
```

`examenes.evento_id` es a la vez PK y FK, igual patrón que
`tareas.evento_id` (extensión 1 a 1 de `eventos`). Crear un examen inserta
primero en `eventos` (con `hora` esta vez no nula) y después en `examenes`.

## Reglas de validación (repetidas de `spec.md`)

- `tema` obligatorio → domain (`crear_examen`).
- `fecha` no puede ser pasada → domain (`crear_examen`).
- `hora` obligatoria → domain (`crear_examen`, `None` rechazado).
- `modalidad` obligatoria → domain (`crear_examen`, `None` rechazado).
- `materia_id` debe existir → service (`CrearExamen`, vía `MateriaRepository`).
