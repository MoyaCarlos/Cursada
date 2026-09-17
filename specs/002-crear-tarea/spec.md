# Feature Specification: Crear Tarea Pendiente (HU-02)

**Feature Branch**: `feature/HU-02-gestion-tareas`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User description: "HU-02: Crear tarea pendiente (materia, título, descripción, fecha límite, prioridad)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crear una tarea pendiente (Priority: P1)

Como usuario, quiero cargar una tarea de una materia con título, descripción,
fecha límite y prioridad, para tener registrado qué me falta entregar.

**Why this priority**: Es el corazón del problema que la app resuelve
(recordar pendientes de la facultad) — sin esto no hay nada que recordar.

**Independent Test**: Se puede probar por completo creando una tarea para
una materia existente y verificando que aparece en el listado, con estado
inicial "pendiente".

**Acceptance Scenarios**:

1. **Given** existe la materia "Bases de Datos",
   **When** el usuario crea una tarea con título "TP1", fecha límite
   "2026-10-15" y prioridad "alta" para esa materia,
   **Then** la tarea queda creada con estado "pendiente" y aparece en el
   listado de tareas.
2. **Given** el usuario está creando una tarea,
   **When** deja el título vacío e intenta guardar,
   **Then** el sistema rechaza la creación y explica que el título es
   obligatorio.
3. **Given** el usuario está creando una tarea,
   **When** elige una fecha límite anterior a hoy,
   **Then** el sistema rechaza la creación y explica que la fecha límite no
   puede ser pasada.
4. **Given** no existe ninguna materia cargada todavía,
   **When** el usuario intenta crear una tarea,
   **Then** el sistema le impide continuar y le indica que primero debe
   crear una materia.

---

### Edge Cases

Reglas en formato EARS:

- **Ubicuo**: El sistema SIEMPRE debe asociar una tarea a exactamente una
  materia existente.
- **Basado en evento**: CUANDO el usuario intenta guardar una tarea con
  título vacío o solo espacios, el sistema DEBE rechazar la operación e
  indicar que el título es obligatorio.
- **Basado en evento**: CUANDO el usuario intenta guardar una tarea con una
  fecha límite anterior a la fecha actual, el sistema DEBE rechazar la
  operación e indicar que la fecha no puede ser pasada.
- **Basado en evento**: CUANDO se crea una tarea sin indicar prioridad, el
  sistema DEBE asignarle prioridad "media" por defecto.
- **Basado en estado**: MIENTRAS no exista ninguna materia cargada, el
  sistema DEBE impedir la creación de tareas.
- **Opcional**: La descripción es opcional; una tarea puede crearse solo con
  título, materia, fecha límite y prioridad.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to create a tarea providing materia,
  título, fecha límite and prioridad, with descripción as optional text.
- **FR-002**: System MUST reject creating a tarea with an empty or
  whitespace-only título.
- **FR-003**: System MUST reject creating a tarea whose fecha límite is
  earlier than the current date.
- **FR-004**: System MUST reject creating a tarea associated with a materia
  that does not exist.
- **FR-005**: System MUST default prioridad to "media" when the user does
  not choose one.
- **FR-006**: System MUST set the initial estado of every new tarea to
  "pendiente".
- **FR-007**: Users MUST be able to view the list of created tareas.

### Key Entities *(include if feature involves data)*

- **Tarea**: Un trabajo pendiente de una Materia (ver `CONTEXT.md`), con
  título, descripción opcional, fecha límite, prioridad (baja/media/alta) y
  estado (pendiente/en progreso/completada — en esta historia siempre nace
  "pendiente"; cambiarlo es HU-04).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un usuario puede cargar una tarea nueva en menos de 20
  segundos, dado que la materia ya existe.
- **SC-002**: El 100% de los intentos de crear una tarea con título vacío o
  fecha pasada son rechazados con un mensaje que explica el motivo.
- **SC-003**: El 100% de las tareas creadas nacen con estado "pendiente" y
  quedan asociadas a la materia correcta.

## Assumptions

- La descripción es texto libre opcional, sin límite de longitud
  particular más allá de uno razonable de interfaz.
- Editar y eliminar una tarea son historias aparte (HU-03); cambiar su
  estado también (HU-04); esta historia solo cubre alta y listado básico.
- No se valida que la fecha límite tenga una hora asociada — es solo fecha
  (sin hora), a diferencia de un Examen.
