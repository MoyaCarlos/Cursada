# Research: Crear Tarea Pendiente (HU-02)

## Evento no se modela como clase de dominio propia

- **Decisión**: `Tarea` es un dataclass "plano" en `domain/tarea.py`
  (materia_id, título, descripción, fecha_límite, prioridad, estado, id) —
  no existe una clase `Evento` en el dominio.
- **Rationale**: `CONTEXT.md` define `Evento` como un concepto técnico
  interno de persistencia (la tabla padre que comparten `Tarea`/`Examen`),
  no como parte del lenguaje ubicuo de cara al usuario ni al dominio. Crear
  una clase `Evento` en Python que nadie instancia por separado sería
  complejidad sin beneficio (KISS). El repositorio de tareas es quien sabe
  que por debajo existen dos tablas (`eventos` + `tareas`) y hace el join.
- **Alternativas consideradas**: modelar `Evento` como clase base de la que
  hereda `Tarea` — descartado porque no hay comportamiento compartido que
  justifique herencia; la relación es solo de persistencia.

## Estado y Prioridad: enum en el dominio, tabla lookup en SQLite

- **Decisión**: `EstadoTarea` y `PrioridadTarea` son `Enum` de Python en el
  dominio. Las tablas `estados`/`prioridades` en SQLite existen igual (ya
  decididas en `docs/modelo-datos.md` para cumplir 3FN) pero se siembran una
  sola vez con valores fijos; el repositorio SQLite traduce entre el enum y
  el `id` de la tabla lookup.
- **Rationale**: cumple el compromiso de 3FN a nivel de esquema sin
  filtrarlo al dominio — el dominio no necesita saber que "pendiente" es el
  id 1 en una tabla; solo conoce el enum.
- **Alternativas consideradas**: exponer los ids de las tablas lookup
  directamente en `Tarea` — descartado porque acoplaría el dominio a un
  detalle de la base de datos (viola Dependency Inversion).

## Validación de "la materia debe existir"

- **Decisión**: vive en el service `CrearTarea`, que depende de
  `MateriaRepository.obtener(materia_id)` además de `TareaRepository`. La
  factory de dominio `crear_tarea()` no consulta repositorios (se mantiene
  pura, sin I/O), solo valida título y fecha.
- **Rationale**: mismo criterio ya aplicado en HU-01 para la unicidad de
  nombre de materia — lo que requiere consultar datos existentes va en el
  service, no en la factory de dominio.

## Fecha límite: solo fecha, sin hora

- **Decisión**: `fecha_limite` es un `date`, no `datetime`. La comparación
  "no puede ser pasada" se hace contra `date.today()`.
- **Rationale**: la spec de HU-02 no pide hora para tareas (a diferencia de
  exámenes, que sí la tienen). Se guarda como texto ISO (`YYYY-MM-DD`) en la
  columna `eventos.fecha`, ya definida así desde HU-01.
