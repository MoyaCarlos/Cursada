# Tasks: Cambiar Estado de una Tarea (HU-04)

Sin Setup ni Foundational nuevos (reutiliza todo lo de HU-01/02/03).

## Phase 1: User Story 1 - Cambiar estado (Priority: P1) 🎯 único incremento

### Tests

- [ ] T001 [P] [US1] `tests/domain/test_tarea.py`: `cambiar_estado_tarea`
  devuelve una tarea con el nuevo estado, preservando el resto de los
  campos, para las 3 transiciones relevantes (incluida "completada" →
  "pendiente", sin restricción).
- [ ] T002 [P] [US1] `tests/services/test_cambiar_estado_tarea.py`:
  `CambiarEstadoTarea` persiste el cambio (usa el fake, verifica
  `obtener(id).estado`).
- [ ] T003 [P] [US1] Escenario BDD en
  `features/cambiar_estado_tarea.feature` (Acceptance Scenarios 1-3),
  steps en `features/steps/test_cambiar_estado_tarea.py`.

### Implementation

- [ ] T004 [US1] En `domain/tarea.py`: `cambiar_estado_tarea(tarea_actual,
  nuevo_estado) -> Tarea`.
- [ ] T005 [US1] Crear `services/cambiar_estado_tarea.py`
  (`CambiarEstadoTarea`): obtiene la tarea, aplica
  `cambiar_estado_tarea()`, guarda con `TareaRepository.actualizar()`.
- [ ] T006 [US1] En `ui/ventana_tareas.py`: combo de estado + botón
  "Cambiar estado", operando sobre la tarea seleccionada en el listado
  (Acceptance Scenario 4: avisa si no hay selección).

**Checkpoint**: HU-04 funcional de punta a punta.

## Phase 2: Polish

- [ ] T007 [P] Correr `quickstart.md` a mano.
- [ ] T008 Revisar el diff antes de mergear.
- [ ] T009 Marcar HU-04 como completada en `docs/backlog.md`.
