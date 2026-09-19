# Research: Editar/Eliminar Examen (HU-07)

Sin decisiones nuevas — esta historia replica exactamente los criterios ya
investigados y aplicados en `specs/003-editar-eliminar-tarea/research.md`,
adaptados a los campos de `Examen`:

- Validar fecha "no pasada" solo si cambia respecto al examen actual
  (mismo criterio que `editar_tarea`).
- Extraer `_validar_tema()` compartida entre `crear_examen` y
  `editar_examen` (mismo criterio que `_validar_titulo()`).
- Borrado real en cascada a `eventos` (mismo criterio que `EliminarTarea`).

La única diferencia real respecto a HU-03: `hora` y `modalidad` se
revalidan como obligatorias en cada edición (no solo al crear), porque a
diferencia de la prioridad de una tarea, no hay un valor por defecto
razonable si alguien las borra del formulario.
