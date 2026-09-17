# Feature Specification: Editar/Eliminar Tarea (HU-03)

**Feature Branch**: `feature/HU-03-editar-eliminar-tarea`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User description: "HU-03: Editar/eliminar una tarea existente."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Editar una tarea existente (Priority: P1)

Como usuario, quiero corregir los datos de una tarea que ya cargué
(materia, título, descripción, fecha límite, prioridad), para arreglar
errores o actualizarla si cambian las condiciones.

**Why this priority**: Es más frecuente corregir una tarea que eliminarla.

**Independent Test**: Se puede probar por completo editando una tarea
existente y verificando que el cambio se refleja en el listado.

**Acceptance Scenarios**:

1. **Given** existe una tarea "TP1" con fecha límite "2026-12-31",
   **When** el usuario edita su título a "TP1 - Entrega final",
   **Then** el listado muestra el nuevo título, sin alterar el resto de sus
   datos.
2. **Given** existe una tarea con fecha límite "2026-12-31",
   **When** el usuario intenta editarla dejando el título vacío,
   **Then** el sistema rechaza la edición y explica que el título es
   obligatorio.
3. **Given** existe una tarea con fecha límite "2026-12-31",
   **When** el usuario intenta cambiar su fecha límite a una fecha ya
   pasada,
   **Then** el sistema rechaza la edición y explica que la fecha límite no
   puede ser pasada.
4. **Given** existe una tarea cuya fecha límite ya pasó (está vencida),
   **When** el usuario la edita sin tocar la fecha límite (por ejemplo,
   solo cambia la descripción),
   **Then** el sistema permite guardar el cambio, sin exigir que la fecha
   ya vencida pase a ser futura.
5. **Given** el usuario está editando una tarea,
   **When** elige asociarla a una materia distinta,
   **Then** el sistema exige que esa materia exista, con la misma regla que
   al crear una tarea.

---

### User Story 2 - Eliminar una tarea existente (Priority: P2)

Como usuario, quiero eliminar una tarea que ya no me sirve (la cargué mal o
ya no aplica), para mantener mi listado limpio.

**Why this priority**: Menos frecuente que editar, pero necesaria.

**Independent Test**: Se puede probar por completo eliminando una tarea
existente y verificando que desaparece del listado.

**Acceptance Scenarios**:

1. **Given** existe una tarea "TP1",
   **When** el usuario la elimina,
   **Then** la tarea deja de aparecer en el listado.

---

### Edge Cases

Reglas en formato EARS:

- **Basado en evento**: CUANDO el usuario intenta guardar una edición con
  título vacío o solo espacios, el sistema DEBE rechazar la operación e
  indicar que el título es obligatorio.
- **Basado en evento**: CUANDO el usuario cambia la fecha límite a una
  fecha anterior a hoy, el sistema DEBE rechazar la operación.
- **Basado en estado**: MIENTRAS la fecha límite no se modifique respecto a
  la que la tarea ya tenía, el sistema NO DEBE exigir que sea una fecha
  futura (permite seguir editando una tarea vencida sin forzar a cambiarle
  la fecha).
- **Basado en evento**: CUANDO el usuario reasigna una tarea a una materia
  que no existe, el sistema DEBE rechazar la operación (misma regla que
  HU-02).
- **No deseado**: SI el usuario elimina una tarea, ENTONCES no debe quedar
  ningún resto de ella (ni en `tareas` ni en `eventos`) que pueda confundir
  a una futura consulta.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to edit título, descripción, fecha límite,
  prioridad and materia of an existing tarea.
- **FR-002**: System MUST reject an edit that leaves título empty or
  whitespace-only.
- **FR-003**: System MUST reject an edit that changes fecha límite to a
  date earlier than today.
- **FR-004**: System MUST NOT reject an edit that leaves fecha límite
  unchanged, even if that date is already in the past.
- **FR-005**: System MUST reject an edit that reassigns the tarea to a
  materia that does not exist.
- **FR-006**: Users MUST be able to delete an existing tarea.
- **FR-007**: System MUST remove all persisted trace of a deleted tarea.

### Key Entities

- **Tarea**: sin cambios respecto a HU-02 — esta historia agrega las
  operaciones de edición y borrado sobre la entidad ya definida.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de las ediciones válidas se reflejan en el listado
  inmediatamente.
- **SC-002**: El 100% de los intentos de edición inválidos (título vacío,
  fecha pasada nueva, materia inexistente) son rechazados con un mensaje
  que explica el motivo.
- **SC-003**: Una tarea eliminada no vuelve a aparecer en ningún listado.

## Assumptions

- No se permite cambiar el estado de la tarea desde esta pantalla de
  edición — eso es HU-04, una historia aparte.
- Eliminar una tarea no tiene restricciones (a diferencia de eliminar una
  materia): no hay ninguna otra entidad que dependa de una tarea todavía.
