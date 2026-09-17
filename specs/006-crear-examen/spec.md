# Feature Specification: Crear Examen (HU-06)

**Feature Branch**: `feature/HU-06-crear-examen`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User description: "HU-06: Crear examen (materia, tema, fecha, hora, modalidad, notas)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crear un examen (Priority: P1)

Como usuario, quiero cargar un examen de una materia con tema, fecha, hora,
modalidad y notas opcionales, para tener registrada la fecha en la que
rindo.

**Why this priority**: Es el segundo tipo de evento del MVP (junto con las
tareas) — sin esto no hay nada que recordar sobre exámenes.

**Independent Test**: Se puede probar por completo creando un examen para
una materia existente y verificando que aparece en el listado de exámenes.

**Acceptance Scenarios**:

1. **Given** existe la materia "Bases de Datos",
   **When** el usuario crea un examen con tema "Parcial 1", fecha
   "2026-11-10", hora "14:00" y modalidad "presencial" para esa materia,
   **Then** el examen queda creado y aparece en el listado de exámenes.
2. **Given** el usuario está creando un examen,
   **When** deja el tema vacío e intenta guardar,
   **Then** el sistema rechaza la creación y explica que el tema es
   obligatorio.
3. **Given** el usuario está creando un examen,
   **When** elige una fecha anterior a hoy,
   **Then** el sistema rechaza la creación y explica que la fecha no puede
   ser pasada.
4. **Given** el usuario está creando un examen,
   **When** no indica una hora,
   **Then** el sistema rechaza la creación y explica que la hora es
   obligatoria (a diferencia de una tarea, un examen sin hora no sirve
   para armar un recordatorio preciso).
5. **Given** no existe ninguna materia cargada todavía,
   **When** el usuario intenta crear un examen,
   **Then** el sistema le impide continuar y le indica que primero debe
   crear una materia.
6. **Given** el usuario carga un examen que es en realidad un recuperatorio
   de otro ya rendido,
   **When** lo guarda,
   **Then** el sistema lo trata como un examen nuevo e independiente, sin
   pedir ni registrar ningún vínculo con el examen original (ver
   `docs/adr/0001-recuperatorio-sin-vinculo.md`).

---

### Edge Cases

Reglas en formato EARS:

- **Ubicuo**: El sistema SIEMPRE debe asociar un examen a exactamente una
  materia existente.
- **Basado en evento**: CUANDO el usuario intenta guardar un examen con
  tema vacío o solo espacios, el sistema DEBE rechazar la operación e
  indicar que el tema es obligatorio.
- **Basado en evento**: CUANDO el usuario intenta guardar un examen con
  fecha anterior a hoy, el sistema DEBE rechazar la operación.
- **Basado en evento**: CUANDO el usuario intenta guardar un examen sin
  hora, el sistema DEBE rechazar la operación.
- **Basado en evento**: CUANDO el usuario intenta guardar un examen sin
  elegir modalidad, el sistema DEBE rechazar la operación (a diferencia de
  la prioridad de una tarea, acá no hay un valor por defecto razonable).
- **Basado en estado**: MIENTRAS no exista ninguna materia cargada, el
  sistema DEBE impedir la creación de exámenes.
- **Opcional**: Las notas son opcionales; un examen puede crearse solo con
  materia, tema, fecha, hora y modalidad.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to create an examen providing materia,
  tema, fecha, hora and modalidad, with notas as optional text.
- **FR-002**: System MUST reject creating an examen with an empty or
  whitespace-only tema.
- **FR-003**: System MUST reject creating an examen whose fecha is earlier
  than the current date.
- **FR-004**: System MUST reject creating an examen without an hora.
- **FR-005**: System MUST reject creating an examen without a modalidad.
- **FR-006**: System MUST reject creating an examen associated with a
  materia that does not exist.
- **FR-007**: Users MUST be able to view the list of created exámenes.

### Key Entities

- **Examen**: Una instancia de evaluación de una Materia (ver
  `CONTEXT.md`), con tema, fecha, hora, modalidad (presencial/virtual) y
  notas opcionales. No tiene un estado propio — se considera completado
  cuando su fecha ya pasó (regla ya definida en `docs/modelo-datos.md`,
  no se reimplementa en esta historia; eso es para cuando exista un
  listado unificado con filtro de completado, HU-16/HU-22).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un usuario puede cargar un examen nuevo en menos de 20
  segundos, dado que la materia ya existe.
- **SC-002**: El 100% de los intentos de crear un examen con tema vacío,
  fecha pasada, sin hora o sin modalidad son rechazados con un mensaje que
  explica el motivo.

## Assumptions

- Las notas son texto libre opcional, sin límite de longitud particular.
- Un recuperatorio se carga como un examen nuevo y corriente, sin ningún
  campo ni relación que lo distinga de un examen regular (ver ADR-0001).
- Editar y eliminar un examen son historias aparte (HU-07); el listado
  unificado con tareas es HU-16, aparte también.
