# Tasks: Editar/Eliminar Examen (HU-07)

## Phase 1: Setup
Ninguno nuevo.

## Phase 2: Foundational

- [ ] T001 Agregar `obtener`, `actualizar`, `eliminar` al `Protocol
  ExamenRepository`.
- [ ] T002 [P] Agregar los mismos 3 métodos a `ExamenRepositoryFake`.

**Checkpoint**: contrato ampliado.

---

## Phase 3: User Story 1 - Editar un examen (Priority: P1) 🎯 MVP

### Tests

- [ ] T003 [P] [US1] `tests/domain/test_examen.py`: `editar_examen`
  rechaza tema vacío; rechaza fecha nueva pasada; permite conservar una
  fecha ya vencida sin cambios; rechaza `hora=None`/`modalidad=None`
  siempre (no solo si cambian).
- [ ] T004 [P] [US1] `tests/services/test_editar_examen.py`:
  `EditarExamen` guarda si la materia existe, rechaza si no.
- [ ] T005 [P] [US1] Escenario BDD en
  `features/editar_eliminar_examen.feature` (Acceptance Scenarios 1-6 de
  US1).

### Implementation

- [ ] T006 [US1] En `domain/examen.py`: extraer `_validar_tema()`;
  implementar `editar_examen(examen_actual, materia_id, tema, fecha,
  hora, modalidad, notas="") -> Examen`.
- [ ] T007 [US1] Implementar `obtener`/`actualizar` en
  `SqliteExamenRepository`.
- [ ] T008 [US1] Crear `services/editar_examen.py` (`EditarExamen`).
- [ ] T009 [US1] En `ui/ventana_examenes.py`: seleccionar y editar (mismo
  patrón que `ventana_tareas.py`: el formulario cambia de modo).

**Checkpoint**: editar funciona de punta a punta.

---

## Phase 4: User Story 2 - Eliminar un examen (Priority: P2)

### Tests

- [ ] T010 [P] [US2] `tests/services/test_eliminar_examen.py`:
  `EliminarExamen` borra el examen del repositorio.
- [ ] T011 [P] [US2] Escenario BDD de eliminar en
  `features/editar_eliminar_examen.feature`.

### Implementation

- [ ] T012 [US2] Implementar `eliminar` en `SqliteExamenRepository`.
- [ ] T013 [US2] Crear `services/eliminar_examen.py` (`EliminarExamen`).
- [ ] T014 [US2] Agregar botón "Eliminar seleccionado" a
  `ui/ventana_examenes.py`, con confirmación.

**Checkpoint**: ambas historias funcionan.

---

## Phase 5: Polish

- [ ] T015 [P] Correr `quickstart.md` a mano.
- [ ] T016 Revisar el diff antes de mergear.
- [ ] T017 Marcar HU-07 como completada en `docs/backlog.md`.
