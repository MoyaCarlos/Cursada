# Tasks: Gestión de Materias (HU-01)

**Input**: Design documents from `specs/001-gestion-materias/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/materia_repository.md

**Tests**: incluidos — la constitución del proyecto exige TDD (ciclo RED/GREEN/REFACTOR) y BDD para toda historia.

**Organization**: tareas agrupadas por historia de usuario (US1 crear, US2 editar, US3 eliminar).

## Phase 1: Setup

- [ ] T001 Crear la estructura de carpetas del proyecto: `domain/`, `services/`, `repository/`, `ui/`, `tests/domain/`, `tests/services/`, `features/steps/`, cada una con un `__init__.py` donde aplique.
- [ ] T002 Crear `requirements-dev.txt` con `pytest` y `pytest-bdd`, e instalarlas.
- [ ] T003 [P] Configurar `pytest.ini` (o sección `[tool.pytest.ini_options]` en `pyproject.toml`) apuntando a `tests/` y `features/` como directorios de test.

---

## Phase 2: Foundational (bloquea todas las historias)

**⚠️ CRITICAL**: ninguna historia puede implementarse sin esto.

- [ ] T004 Implementar `repository/db.py`: resuelve la ruta del archivo SQLite según el SO (Linux: `$XDG_DATA_HOME/cursada/cursada.db` con fallback a `~/.local/share/cursada/cursada.db`; Windows: `%APPDATA%\Cursada\cursada.db`, ver `research.md`) y expone una función `conectar()` que abre la conexión.
- [ ] T005 En `repository/db.py`, agregar `crear_tablas(conexion)` que ejecuta `CREATE TABLE IF NOT EXISTS` para `materias (id, nombre, nombre_normalizado)` con `nombre_normalizado TEXT NOT NULL UNIQUE`, y `eventos (id, materia_id, titulo, fecha, hora)` con `materia_id` como `REFERENCES materias(id)`, exactamente como en `data-model.md`.
- [ ] T006 [P] Crear `domain/materia.py` con el dataclass `Materia` (`id: int | None`, `nombre: str`).
- [ ] T007 [P] Crear `repository/materia_repository.py` con el `Protocol MateriaRepository` (`guardar`, `existe_nombre`, `listar`, `obtener`, `eliminar`, `tiene_eventos_asociados`) tal como está definido en `contracts/materia_repository.md`.
- [ ] T008 Implementar `repository/sqlite_materia_repository.py` (`SqliteMateriaRepository`) cumpliendo el Protocol de T007 contra las tablas de T005.
- [ ] T009 [P] Crear un fake en memoria del `MateriaRepository` en `tests/fakes.py`, para testear servicios sin tocar disco.

**Checkpoint**: con esto, cualquier historia de usuario puede implementarse.

---

## Phase 3: User Story 1 - Crear una materia (Priority: P1) 🎯 MVP

**Goal**: el usuario puede crear una materia con nombre único y verla en el listado.

**Independent Test**: crear una materia con un nombre y verificar que aparece en el listado; intentar crear un nombre vacío o duplicado y verificar que se rechaza.

### Tests for User Story 1

> Escribir estos tests primero y confirmar que fallan (RED) antes de implementar.

- [ ] T010 [P] [US1] Test de dominio en `tests/domain/test_materia.py`: `crear_materia("")` y `crear_materia("   ")` deben rechazarse — regla "nombre obligatorio, no vacío ni solo espacios" (FR-002).
- [ ] T011 [P] [US1] Test de servicio en `tests/services/test_crear_materia.py`, usando el fake de T009: `CrearMateria` rechaza un nombre que ya existe comparando "sin distinguir mayúsculas/minúsculas ni espacios al inicio/final" (FR-003).
- [ ] T012 [P] [US1] Escenario BDD "Crear una materia" (los 3 `Acceptance Scenarios` de US1 en `spec.md`) en `features/gestion_materias.feature`, con sus steps en `features/steps/test_gestion_materias.py`.

### Implementation for User Story 1

- [ ] T013 [US1] En `domain/materia.py`, agregar la factory `crear_materia(nombre: str) -> Materia` que aplica `.strip()` y rechaza (`ValueError`) nombre vacío (T010 en verde).
- [ ] T014 [US1] Crear `services/crear_materia.py` (`CrearMateria`): consulta `repository.existe_nombre(nombre)` (T011 en verde), y si no existe, llama a `crear_materia()` y `repository.guardar()` (FR-001).
- [ ] T015 [US1] Crear `ui/ventana_materias.py`: ventana Tkinter con listado de materias (`repository.listar()`, FR-005) y formulario para crear una nueva, mostrando el error de `CrearMateria` si lo rechaza.
- [ ] T016 [US1] Crear `main.py`: conecta a la base (T004), crea las tablas (T005), instancia `SqliteMateriaRepository` y `CrearMateria`, y abre `ventana_materias`.

**Checkpoint**: User Story 1 funcional de punta a punta — se puede correr `python3 main.py` y crear materias.

---

## Phase 4: User Story 2 - Editar el nombre de una materia (Priority: P2)

**Goal**: el usuario puede corregir el nombre de una materia existente.

**Independent Test**: editar el nombre de una materia existente y verificar que el cambio se refleja; intentar editarlo a un nombre que ya usa otra materia y verificar que se rechaza.

### Tests for User Story 2

- [ ] T017 [P] [US2] Test de servicio en `tests/services/test_editar_materia.py`, usando el fake de T009: `EditarMateria` rechaza el nuevo nombre si ya lo usa **otra** materia, pero permite guardar sin cambios si el nombre no varió.
- [ ] T018 [P] [US2] Escenario BDD "Editar el nombre de una materia" (los 2 `Acceptance Scenarios` de US2 en `spec.md`), agregado a `features/gestion_materias.feature`.

### Implementation for User Story 2

- [ ] T019 [US2] Crear `services/editar_materia.py` (`EditarMateria`): llama a `repository.existe_nombre(nuevo_nombre, excluir_id=id)` antes de guardar (FR-003, FR-004).
- [ ] T020 [US2] Agregar edición a `ui/ventana_materias.py`: seleccionar una materia del listado y editar su nombre, mostrando el error si `EditarMateria` la rechaza.

**Checkpoint**: User Stories 1 y 2 funcionan de forma independiente.

---

## Phase 5: User Story 3 - Eliminar una materia (Priority: P3)

**Goal**: el usuario puede eliminar una materia sin tareas/exámenes asociados; no puede eliminar una que sí los tiene.

**Independent Test**: eliminar una materia sin eventos asociados (debe desaparecer del listado); intentar eliminar una con al menos un evento asociado (debe bloquearse con mensaje).

### Tests for User Story 3

- [ ] T021 [P] [US3] Test de repositorio (contra SQLite real, no el fake) en `tests/repository/test_sqlite_materia_repository.py`: `tiene_eventos_asociados` devuelve `True` solo si hay una fila en `eventos` con ese `materia_id`.
- [ ] T022 [P] [US3] Test de servicio en `tests/services/test_eliminar_materia.py`, usando el fake de T009: `EliminarMateria` bloquea la eliminación "MIENTRAS una materia tenga al menos una tarea o examen asociado" (regla basada en estado de `spec.md`) y elimina si no tiene ninguno (FR-006).
- [ ] T023 [P] [US3] Escenario BDD "Eliminar una materia" (los 2 `Acceptance Scenarios` de US3 en `spec.md`), agregado a `features/gestion_materias.feature`.

### Implementation for User Story 3

- [ ] T024 [US3] En `repository/sqlite_materia_repository.py`, implementar `tiene_eventos_asociados(materia_id)` con `SELECT 1 FROM eventos WHERE materia_id = ? LIMIT 1`.
- [ ] T025 [US3] Crear `services/eliminar_materia.py` (`EliminarMateria`): si `repository.tiene_eventos_asociados(id)` es `True`, rechaza con un mensaje que explica el motivo (FR-007); si no, llama a `repository.eliminar(id)`.
- [ ] T026 [US3] Agregar botón "Eliminar" a `ui/ventana_materias.py`, mostrando el mensaje de bloqueo cuando corresponda.

**Checkpoint**: las 3 historias de HU-01 funcionan de punta a punta.

---

## Phase 6: Polish

- [ ] T027 [P] Correr manualmente los 4 pasos de `quickstart.md` y confirmar que el resultado coincide con lo esperado.
- [ ] T028 Revisar el diff completo de la rama `feature/HU-01-gestion-materias` (autor revisa su propio diff, per Definition of Done — no hay otro integrante).
- [ ] T029 Marcar HU-01 como completada en `docs/backlog.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sin dependencias.
- **Foundational (Phase 2)**: depende de Setup — bloquea las 3 historias.
- **User Stories (Phase 3-5)**: dependen de Foundational. US2 y US3 reutilizan `ui/ventana_materias.py` creado en US1 (misma ventana, se va ampliando), por eso conviene implementarlas en orden P1 → P2 → P3 en un proyecto de una sola persona, aunque cada una es testeable de forma independiente a nivel de dominio/servicio.
- **Polish (Phase 6)**: depende de que estén completas las historias que se vayan a entregar (mínimo US1 para el MVP).

### Parallel Opportunities

- T006, T007, T009 (Phase 2) — archivos distintos, sin dependencias entre sí.
- Dentro de cada historia, las tareas marcadas [P] (tests de distintos archivos) pueden hacerse en paralelo entre sí, pero todas antes que las tareas de implementación de esa misma historia (RED antes que GREEN).

---

## Implementation Strategy

### MVP First

1. Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1).
2. Parar y validar US1 de forma independiente (`quickstart.md`, pasos 1-2).
3. Ese es el MVP demostrable de HU-01.

### Incremental Delivery

4. Agregar US2 (editar) → validar → commitear.
5. Agregar US3 (eliminar) → validar → commitear.
6. Phase 6 (Polish) al final, antes de mergear a `main`.

Cada tarea (o grupo chico de tareas relacionadas) es un commit; los tests
(T010-T012, T017-T018, T021-T023) se commitean como `RED:`, la
implementación correspondiente como `GREEN:`, y cualquier limpieza
posterior como `REFACTOR:` — según la convención de la constitución.
