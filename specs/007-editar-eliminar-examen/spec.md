# Feature Specification: Editar/Eliminar Examen (HU-07)

**Feature Branch**: `feature/HU-07-editar-eliminar-examen`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User description: "HU-07: Editar/eliminar un examen existente."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Editar un examen existente (Priority: P1)

Como usuario, quiero corregir los datos de un examen que ya cargué
(materia, tema, fecha, hora, modalidad, notas), para arreglar errores o
actualizarlo si cambian las condiciones (ej: se reprograma la fecha).

**Why this priority**: Más frecuente que eliminarlo.

**Independent Test**: Se puede probar por completo editando un examen
existente y verificando que el cambio se refleja en el listado.

**Acceptance Scenarios**:

1. **Given** existe un examen "Parcial 1" con fecha "2026-11-10",
   **When** el usuario edita su tema a "Parcial 1 - Reprogramado",
   **Then** el listado muestra el nuevo tema.
2. **Given** existe un examen,
   **When** el usuario intenta editarlo dejando el tema vacío,
   **Then** el sistema rechaza la edición.
3. **Given** existe un examen,
   **When** el usuario intenta cambiar su fecha a una fecha ya pasada,
   **Then** el sistema rechaza la edición (esto es "reprogramar", ver
   `CONTEXT.md` — sigue siendo el mismo examen).
4. **Given** existe un examen cuya fecha ya pasó,
   **When** el usuario lo edita sin tocar la fecha (por ejemplo, cambia
   solo las notas),
   **Then** el sistema lo permite, sin exigir que la fecha pase a ser
   futura.
5. **Given** el usuario está editando un examen,
   **When** borra la hora o la modalidad,
   **Then** el sistema rechaza la edición (siguen siendo obligatorias,
   igual que al crear).
6. **Given** el usuario está editando un examen,
   **When** elige asociarlo a una materia distinta,
   **Then** el sistema exige que esa materia exista.

---

### User Story 2 - Eliminar un examen existente (Priority: P2)

Como usuario, quiero eliminar un examen que cargué mal o ya no aplica.

**Why this priority**: Menos frecuente que editar.

**Independent Test**: Eliminar un examen existente y verificar que
desaparece del listado.

**Acceptance Scenarios**:

1. **Given** existe un examen "Parcial 1",
   **When** el usuario lo elimina,
   **Then** deja de aparecer en el listado.

---

### Edge Cases

- **Basado en evento**: CUANDO el usuario guarda una edición con tema
  vacío, hora vacía o sin modalidad, el sistema DEBE rechazar la
  operación (mismas reglas que al crear, HU-06).
- **Basado en evento**: CUANDO el usuario cambia la fecha a una anterior a
  hoy, el sistema DEBE rechazar la operación.
- **Basado en estado**: MIENTRAS la fecha no se modifique respecto a la
  que el examen ya tenía, el sistema NO DEBE exigir que sea futura (mismo
  criterio que HU-03 para tareas).
- **No deseado**: SI el usuario elimina un examen, ENTONCES no debe quedar
  ningún resto de él (ni en `examenes` ni en `eventos`).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to edit materia, tema, fecha, hora,
  modalidad and notas of an existing examen.
- **FR-002**: System MUST reject an edit that leaves tema empty, hora
  empty, or modalidad unset — same rules as creating (HU-06).
- **FR-003**: System MUST reject an edit that changes fecha to a date
  earlier than today.
- **FR-004**: System MUST NOT reject an edit that leaves fecha unchanged,
  even if that date is already in the past.
- **FR-005**: System MUST reject an edit that reassigns the examen to a
  materia that does not exist.
- **FR-006**: Users MUST be able to delete an existing examen.
- **FR-007**: System MUST remove all persisted trace of a deleted examen.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de las ediciones válidas se reflejan de inmediato.
- **SC-002**: El 100% de las ediciones inválidas son rechazadas con un
  mensaje que explica el motivo.
- **SC-003**: Un examen eliminado no vuelve a aparecer en ningún listado.

## Assumptions

- Igual que HU-03: eliminar un examen no tiene restricciones (nada
  depende de un examen todavía).
- Reprogramar (editar la fecha del mismo examen) sigue siendo distinto de
  cargar un recuperatorio (un examen nuevo) — ver
  `docs/adr/0001-recuperatorio-sin-vinculo.md` y `CONTEXT.md`.
