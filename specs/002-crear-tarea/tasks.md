# Tasks: Crear Tarea Pendiente (HU-02)

**Input**: Design documents from `specs/002-crear-tarea/`

**Tests**: incluidos (constitución exige TDD/BDD).

## Phase 1: Setup

Reutiliza el entorno de HU-01 (venv, pytest, pytest-bdd, `tk`) — sin tareas
nuevas.

---

## Phase 2: Foundational (bloquea la historia)

- [ ] T001 En `repository/db.py`, agregar a `crear_tablas()`: `estados` y
  `prioridades` (lookup, sembradas con `INSERT OR IGNORE` según
  `data-model.md`), y `tareas` (`evento_id` PK/FK a `eventos`, `descripcion`,
  `estado_id`, `prioridad_id`).
- [ ] T002 [P] Crear `domain/tarea.py` con los enums `EstadoTarea` y
  `PrioridadTarea`, y el dataclass `Tarea` (`materia_id`, `titulo`,
  `descripcion`, `fecha_limite`, `prioridad`, `estado`, `id`).
- [ ] T003 [P] Crear `repository/tarea_repository.py` con el `Protocol
  TareaRepository` (`guardar`, `listar`) tal como en `contracts/tarea_repository.md`.
- [ ] T004 Implementar `repository/sqlite_tarea_repository.py`
  (`SqliteTareaRepository`): `guardar()` inserta en `eventos` y `tareas` en
  la misma llamada; `listar()` hace el join `eventos ⋈ tareas ⋈ estados ⋈
  prioridades` y arma objetos `Tarea`.
- [ ] T005 [P] Agregar `TareaRepositoryFake` a `tests/fakes.py`, mismo
  contrato que T003, en memoria.

**Checkpoint**: infraestructura lista para la historia.

---

## Phase 3: User Story 1 - Crear una tarea pendiente (Priority: P1) 🎯 MVP

**Goal**: el usuario carga una tarea con materia/título/fecha/prioridad y la
ve en el listado, con estado inicial "pendiente".

**Independent Test**: crear una tarea para una materia existente y
verificar que aparece con estado "pendiente"; intentar con título vacío,
fecha pasada, o sin ninguna materia cargada, y verificar el rechazo.

### Tests for User Story 1

- [ ] T006 [P] [US1] Test de dominio en `tests/domain/test_tarea.py`:
  `crear_tarea` rechaza título vacío/solo espacios (FR-002), rechaza fecha
  límite anterior a hoy (FR-003), usa prioridad "media" por defecto
  (FR-005), y siempre nace con estado "pendiente" (FR-006).
- [ ] T007 [P] [US1] Test de servicio en `tests/services/test_crear_tarea.py`,
  con `TareaRepositoryFake` + `MateriaRepositoryFake`: `CrearTarea` guarda
  cuando la materia existe, y rechaza (sin guardar) si la materia no existe
  (FR-004).
- [ ] T008 [P] [US1] Escenario BDD en `features/crear_tarea.feature` (los 4
  `Acceptance Scenarios` de `spec.md`), con steps en
  `features/steps/test_crear_tarea.py`.

### Implementation for User Story 1

- [ ] T009 [US1] En `domain/tarea.py`, implementar `crear_tarea(materia_id,
  titulo, fecha_limite, descripcion="", prioridad=PrioridadTarea.MEDIA) ->
  Tarea`, con las validaciones de T006 (T006 en verde).
- [ ] T010 [US1] Crear `services/crear_tarea.py` (`CrearTarea`): depende de
  `TareaRepository` y `MateriaRepository`; valida
  `materia_repositorio.obtener(materia_id) is not None` antes de llamar a
  `crear_tarea()` y `tarea_repositorio.guardar()` (T007 en verde).
- [ ] T011 [US1] Crear `ui/ventana_tareas.py`: selector de materia
  (poblado desde `MateriaRepository.listar()`), campos título/descripción/
  fecha límite/prioridad, botón "Crear tarea", listado de tareas
  existentes (FR-007). Si no hay materias cargadas, deshabilita el alta y
  lo indica (regla "basado en estado" de `spec.md`).
- [ ] T012 [US1] Actualizar `main.py`: instanciar `SqliteTareaRepository`,
  `CrearTarea`, y abrir `ventana_tareas` (además de `ventana_materias` —
  ver decisión de UI en el commit de implementación).

**Checkpoint**: HU-02 funcional de punta a punta.

---

## Phase 4: Polish

- [ ] T013 [P] Correr `quickstart.md` a mano y confirmar el resultado.
- [ ] T014 Revisar el diff completo de la rama antes de mergear.
- [ ] T015 Marcar HU-02 como completada en `docs/backlog.md`.

---

## Dependencies & Execution Order

- Setup: ninguno nuevo. Foundational (T001-T005) bloquea la historia.
- Dentro de la historia: tests (T006-T008) antes que implementación
  (T009-T012), RED antes que GREEN.
- T009 y T010 en secuencia (el service depende de la factory). T011 depende
  de T010. T012 depende de T011.

## Implementation Strategy

Setup (reutilizado) → Foundational → US1 (RED → GREEN) → Polish. Un solo
incremento: no hay US2/US3 en esta historia.
