# Tasks: Editar/Eliminar Tarea (HU-03)

## Phase 1: Setup

Ninguno nuevo (reutiliza HU-01/HU-02).

## Phase 2: Foundational

- [ ] T001 En `repository/tarea_repository.py`, agregar `obtener`,
  `actualizar`, `eliminar` al `Protocol` (ver `contracts/tarea_repository.md`).
- [ ] T002 [P] Agregar `obtener`, `actualizar`, `eliminar` a
  `TareaRepositoryFake` en `tests/fakes.py`.

**Checkpoint**: contrato ampliado, listo para ambas historias.

---

## Phase 3: User Story 1 - Editar una tarea (Priority: P1) 🎯 MVP

### Tests

- [ ] T003 [P] [US1] `tests/domain/test_tarea.py`: `editar_tarea` rechaza
  título vacío; rechaza fecha límite nueva anterior a hoy; **permite**
  guardar si la fecha límite no cambió aunque ya esté vencida (FR-004).
- [ ] T004 [P] [US1] `tests/services/test_editar_tarea.py`: `EditarTarea`
  guarda cuando la materia (nueva o igual) existe; rechaza si la materia
  no existe.
- [ ] T005 [P] [US1] Escenario BDD en `features/editar_eliminar_tarea.feature`
  (Acceptance Scenarios 1-5 de US1), steps en
  `features/steps/test_editar_eliminar_tarea.py`.

### Implementation

- [ ] T006 [US1] En `domain/tarea.py`: extraer `_validar_titulo()` (usada
  por `crear_tarea` y la nueva `editar_tarea`); implementar
  `editar_tarea(tarea_actual, materia_id, titulo, fecha_limite,
  descripcion, prioridad) -> Tarea`.
- [ ] T007 [US1] Implementar `obtener`/`actualizar` en
  `SqliteTareaRepository` (UPDATE en `eventos` + `tareas`).
- [ ] T008 [US1] Crear `services/editar_tarea.py` (`EditarTarea`): obtiene
  la tarea actual, valida materia, llama a `editar_tarea()` del dominio y
  `actualizar()` del repositorio.
- [ ] T009 [US1] En `ui/ventana_tareas.py`: seleccionar una tarea del
  listado y editarla (reutilizar el formulario existente).

**Checkpoint**: editar funciona de punta a punta.

---

## Phase 4: User Story 2 - Eliminar una tarea (Priority: P2)

### Tests

- [ ] T010 [P] [US2] `tests/services/test_eliminar_tarea.py`:
  `EliminarTarea` borra la tarea del repositorio.
- [ ] T011 [P] [US2] Escenario BDD de eliminar en
  `features/editar_eliminar_tarea.feature`.

### Implementation

- [ ] T012 [US2] Implementar `eliminar` en `SqliteTareaRepository` (borra
  `tareas` y `eventos`).
- [ ] T013 [US2] Crear `services/eliminar_tarea.py` (`EliminarTarea`).
- [ ] T014 [US2] Agregar botón "Eliminar seleccionada" a
  `ui/ventana_tareas.py`, con confirmación.

**Checkpoint**: ambas historias de HU-03 funcionan.

---

## Phase 5: Polish

- [ ] T015 [P] Correr `quickstart.md` a mano.
- [ ] T016 Revisar el diff completo antes de mergear.
- [ ] T017 Marcar HU-03 como completada en `docs/backlog.md`.

## Dependencies

Foundational (T001-T002) bloquea ambas historias. Dentro de cada una:
tests antes que implementación (RED antes que GREEN). US2 reutiliza el
`_materias_listadas`/selección de la UI que US1 deja armada.
