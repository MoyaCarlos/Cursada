# Research: Ventana Principal con Vista Unificada (HU-16)

## `ItemPendiente` vive en `services/`, no en `domain/`

- **Decisión**: la fila combinada que muestra la vista unificada (tipo,
  materia, título, fecha, estado) es un dataclass `ItemPendiente`
  definido junto al service `ListarPendientes` en
  `services/listar_pendientes.py`, no una clase de `domain/`.
- **Rationale**: no representa una regla de negocio ni un invariante que
  proteger — es una proyección de solo lectura armada combinando `Tarea`
  y `Examen`, que ya existen y ya validan sus propias reglas. `CONTEXT.md`
  ya había decidido que `Evento` es un concepto técnico interno que ni
  siquiera necesita ser una clase de dominio (ver
  `specs/002-crear-tarea/research.md`); `ItemPendiente` es un caso
  parecido, un paso más: ni siquiera es la tabla compartida, es solo la
  fila que la UI necesita para pintar el listado.
- **Alternativas consideradas**: crear finalmente una clase `Evento` de
  dominio unificando `Tarea`/`Examen` — descartada por la misma razón que
  ya se descartó en HU-02: no hay comportamiento compartido que
  justifique una jerarquía, y forzaría a `Tarea`/`Examen` a heredar de
  algo que hoy no necesitan.

## Consolidar las 3 ventanas en pestañas (decisión diferida desde HU-02)

- **Decisión**: `VentanaMaterias`, `VentanaTareas` y `VentanaExamenes`
  dejan de ser ventanas Tk propias (`tk.Tk`/`tk.Toplevel`) y pasan a ser
  `ttk.Frame` (renombradas `PanelMaterias`, `PanelTareas`,
  `PanelExamenes`), montadas como pestañas de un único `ttk.Notebook` en
  una nueva `VentanaPrincipal`. Se agrega una cuarta pestaña
  `PanelPendientes` con el listado unificado.
- **Rationale**: cuando se probó HU-02 por primera vez, se preguntó
  explícitamente si se podía consolidar todo en una sola ventana con
  paneles. La respuesta en ese momento fue esperar a HU-16 para no
  construir un shell de pestañas que HU-16 iba a terminar rehaciendo —
  este es exactamente ese momento.
- **Riesgo cubierto**: ningún test automatizado importa
  `VentanaMaterias`/`VentanaTareas`/`VentanaExamenes` por nombre (se
  verificó con grep sobre `tests/` y `features/` antes de tocar nada),
  así que renombrar las clases no rompe la suite — solo hace falta
  verificar manualmente la UI resultante.
- **Refresco al cambiar de pestaña**: cada panel expone un método público
  `actualizar()` (refresca su combo de materias y su listado);
  `VentanaPrincipal` se suscribe al evento `<<NotebookTabChanged>>` del
  Notebook y llama `actualizar()` del panel recién seleccionado. Evita
  que, por ejemplo, la pestaña Tareas muestre una lista de materias
  desactualizada si se creó una materia nueva en la pestaña Materias.
- **Alternativas consideradas**: mantener las 3 ventanas sueltas y solo
  agregar una cuarta — descartada porque no resuelve el pedido de UX ya
  planteado, y porque HU-16 explícitamente pide "ventana principal"
  (singular).
