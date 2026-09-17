# Research: Crear Examen (HU-06)

## Reubicar `MateriaInexistenteError` a `domain/materia.py`

- **Decisión**: mover la excepción desde `domain/tarea.py` a
  `domain/materia.py`. `domain/tarea.py` pasa a importarla desde ahí.
- **Rationale**: la excepción representa una regla sobre `Materia`
  ("no existe una materia con este id"), no sobre `Tarea`. Vivía en
  `tarea.py` porque fue la primera en necesitarla (HU-02); ahora que
  `Examen` también la necesita, dejarla en `tarea.py` obligaría a
  `domain/examen.py` a importar de `domain/tarea.py` para algo que no
  tiene que ver con tareas — acoplamiento incorrecto. Es el mismo tipo de
  ajuste que ya hizo la skill `domain-modeling` con "reprogramar" vs.
  "recuperatorio": el nombre correcto en el lugar correcto.

## `hora` y `modalidad` obligatorios: `None` como sentinel

- **Decisión**: `crear_examen(..., hora: time | None, modalidad:
  ModalidadExamen | None, ...)` acepta `None` para representar "el
  usuario no completó este campo", y lo valida como cualquier otra regla
  de negocio (mismo lugar que el título vacío de una tarea).
- **Rationale**: consistente con cómo `crear_tarea` valida título vacío —
  la UI siempre puede construir el valor tipado correcto (`time`,
  `ModalidadExamen`) o pasar `None` si el campo quedó sin completar, sin
  necesitar un tipo de "vacío" por separado para cada campo.

## `modalidades`: lookup igual que `estados`/`prioridades`

- **Decisión**: tabla `modalidades (id, nombre)` sembrada con
  `presencial`/`virtual`, igual patrón que `estados`/`prioridades` de
  HU-02. `ModalidadExamen` es un enum en el dominio; el repositorio
  traduce contra la tabla, igual que ya hace `SqliteTareaRepository` con
  estado/prioridad.
- **Rationale**: ya está decidido en `docs/modelo-datos.md` (3FN); esta
  historia solo la crea en `db.py`, sin decisiones nuevas de esquema.

## `eventos.hora` sigue siendo nullable

- **Decisión**: la columna `eventos.hora` (creada en HU-01) no cambia —
  sigue permitiendo `NULL`, porque las tareas no la usan. La obligatoriedad
  de `hora` para un examen se valida en el dominio (`crear_examen`), no en
  el esquema.
- **Rationale**: `eventos` es la tabla compartida por `Tarea` y `Examen`
  (ver `CONTEXT.md`); una regla que solo aplica a uno de los dos tipos no
  debe convertirse en una restricción de la tabla compartida.
