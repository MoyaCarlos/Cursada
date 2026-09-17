# Tasks: Crear Examen (HU-06)

## Phase 1: Setup

Ninguno nuevo.

## Phase 2: Foundational

- [ ] T001 Reubicar `MateriaInexistenteError` de `domain/tarea.py` a
  `domain/materia.py`; actualizar imports en `domain/tarea.py`,
  `services/crear_tarea.py`, `services/editar_tarea.py` y sus tests/BDD.
  Correr toda la suite para confirmar que sigue en 50/50 verde tras el
  refactor.
- [ ] T002 En `repository/db.py`, agregar tablas `modalidades` (lookup,
  sembrada) y `examenes` (evento_id PK/FK, modalidad_id, notas).
- [ ] T003 [P] Crear `domain/examen.py` con `ModalidadExamen` (enum) y el
  dataclass `Examen` (sin factory todavía).
- [ ] T004 [P] Crear `repository/examen_repository.py` (`Protocol`,
  ver `contracts/examen_repository.md`).
- [ ] T005 Implementar `repository/sqlite_examen_repository.py`.
- [ ] T006 [P] Agregar `ExamenRepositoryFake` a `tests/fakes.py`.

**Checkpoint**: infraestructura lista.

---

## Phase 3: User Story 1 - Crear un examen (Priority: P1) 🎯 MVP

### Tests

- [ ] T007 [P] [US1] `tests/domain/test_examen.py`: `crear_examen` rechaza
  tema vacío, fecha pasada, `hora=None`, `modalidad=None`.
- [ ] T008 [P] [US1] `tests/services/test_crear_examen.py`: `CrearExamen`
  guarda si la materia existe, rechaza si no.
- [ ] T009 [P] [US1] Escenario BDD en `features/crear_examen.feature`
  (Acceptance Scenarios 1-5; el 6 -recuperatorio- no requiere un escenario
  nuevo: ya lo cubre "crear un examen" sin ningún campo extra).

### Implementation

- [ ] T010 [US1] En `domain/examen.py`: `crear_examen(materia_id, tema,
  fecha, hora, modalidad, notas="") -> Examen`.
- [ ] T011 [US1] Crear `services/crear_examen.py` (`CrearExamen`).
- [ ] T012 [US1] Crear `ui/ventana_examenes.py`: selector de materia,
  tema, fecha, hora, modalidad, notas opcional, listado.
- [ ] T013 [US1] Actualizar `main.py`: wiring de exámenes.

**Checkpoint**: HU-06 funcional de punta a punta.

---

## Phase 4: Polish

- [ ] T014 [P] Correr `quickstart.md` a mano.
- [ ] T015 Revisar el diff antes de mergear.
- [ ] T016 Marcar HU-06 como completada en `docs/backlog.md`.
