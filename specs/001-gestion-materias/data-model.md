# Data Model: Gestión de Materias (HU-01)

## Materia

Ver definición de dominio en `CONTEXT.md`.

| Campo    | Tipo    | Reglas                                                        |
|----------|---------|----------------------------------------------------------------|
| `id`     | integer | Generado por la base de datos, autoincremental.                |
| `nombre` | text    | Obligatorio. No vacío ni solo espacios. Único (comparación sin distinguir mayúsculas/minúsculas ni espacios al inicio/final). |

**Tablas SQLite creadas en esta historia** (ver `docs/modelo-datos.md` para
el esquema completo del proyecto, que se completa incrementalmente):

```sql
CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    nombre_normalizado TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    materia_id INTEGER NOT NULL REFERENCES materias(id),
    titulo TEXT NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT
);
```

`eventos` se crea acá (vacía) porque FR-007 de esta historia depende de
poder consultarla (`tiene_eventos_asociados`), aunque todavía nadie inserte
filas en ella — recién HU-02 (tareas) y HU-06 (exámenes) van a insertar ahí.
No se crean `tareas` ni `examenes` en esta historia: esas tablas extienden
`eventos` y se agregan cuando esas historias lo necesiten.

`nombre_normalizado` guarda `nombre.strip().lower()` — permite que SQLite
haga cumplir la unicidad case-insensitive con una restricción `UNIQUE`
nativa, en vez de reimplementar la comprobación a mano en cada operación.
Es un detalle de la implementación del adaptador SQLite, no un campo del
dominio: `Materia` (la entidad) solo expone `id` y `nombre`.

## Transiciones de estado

No aplica — `Materia` no tiene estados, solo existe o no existe (alta/edición/baja).

## Reglas de validación (repetidas de `spec.md` para referencia rápida)

- Nombre obligatorio (no vacío, no solo espacios) → domain (`crear_materia`).
- Nombre único, case-insensitive → service, vía `MateriaRepository.existe_nombre`.
- No se puede eliminar una materia con tareas o exámenes asociados → service
  (`EliminarMateria`), vía `MateriaRepository.tiene_eventos_asociados`, que
  consulta la tabla `eventos` real (creada en esta historia, ver arriba).
  Hoy siempre devuelve `False` porque nada inserta filas en `eventos`
  todavía — empieza a tener efecto real cuando HU-02/HU-06 empiecen a crear
  tareas/exámenes.
