# Feature Specification: Cambiar Estado de una Tarea (HU-04)

**Feature Branch**: `feature/HU-04-cambiar-estado-tarea`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User description: "HU-04: Cambiar el estado de una tarea (pendiente / en progreso / completada)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cambiar el estado de una tarea (Priority: P1)

Como usuario, quiero marcar una tarea como "en progreso" o "completada" (o
volverla a "pendiente"), para reflejar en qué anda cada trabajo.

**Why this priority**: Es la única historia de esta feature.

**Independent Test**: Se puede probar por completo seleccionando una tarea,
cambiándole el estado, y verificando que el listado lo refleja.

**Acceptance Scenarios**:

1. **Given** una tarea con estado "pendiente",
   **When** el usuario le cambia el estado a "en_progreso",
   **Then** el listado muestra la tarea con estado "en_progreso".
2. **Given** una tarea con estado "en_progreso",
   **When** el usuario le cambia el estado a "completada",
   **Then** el listado la muestra "completada".
3. **Given** una tarea con estado "completada",
   **When** el usuario le cambia el estado de vuelta a "pendiente",
   **Then** el sistema lo permite (no hay transiciones restringidas: se
   puede pasar de cualquier estado a cualquier otro).
4. **Given** el usuario no seleccionó ninguna tarea del listado,
   **When** intenta cambiar el estado,
   **Then** el sistema le pide que seleccione una tarea primero.

---

### Edge Cases

- **Ubicuo**: El sistema SIEMPRE permite cualquier transición entre
  "pendiente", "en_progreso" y "completada" — no existe una máquina de
  estados restringida (es una herramienta de seguimiento personal, no de
  aprobación).
- **Basado en evento**: CUANDO el usuario intenta cambiar el estado sin
  haber seleccionado una tarea, el sistema DEBE avisarle que seleccione una.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to change the estado of a selected tarea
  to any of "pendiente", "en_progreso", "completada".
- **FR-002**: System MUST allow any transition between the three estados,
  without restrictions.
- **FR-003**: Changes MUST be reflected in the tareas listing immediately.

### Key Entities

- **Tarea**: sin cambios de estructura — esta historia solo agrega la
  operación de cambiar su campo `estado`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los cambios de estado se reflejan de inmediato en
  el listado.
- **SC-002**: Un usuario puede cambiar el estado de una tarea en menos de 5
  segundos.

## Assumptions

- No se pide confirmación para cambiar el estado (a diferencia de eliminar
  una tarea) — es una operación de bajo riesgo y fácilmente reversible.
- No se valida ninguna relación entre el nuevo estado y la fecha límite
  (por ejemplo, no se impide marcar "completada" una tarea vencida, ni se
  fuerza a "pendiente" una tarea con fecha futura).
