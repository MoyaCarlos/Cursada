# Feature Specification: Gestión de Materias (HU-01)

**Feature Branch**: `feature/HU-01-gestion-materias`

**Created**: 2026-09-16

**Status**: Draft

**Input**: User description: "HU-01: Como usuario quiero crear, editar y eliminar materias para organizar tareas y exámenes por asignatura."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crear una materia (Priority: P1)

Como usuario, quiero crear una materia nueva indicando su nombre, para poder
después asociarle tareas y exámenes.

**Why this priority**: Sin materias no se puede cargar ninguna tarea ni
examen — es el prerequisito de todo lo demás en el backlog.

**Independent Test**: Se puede probar por completo creando una materia con
un nombre y verificando que aparece en el listado. Entrega valor por sí sola
(organización básica), incluso sin edición ni eliminación.

**Acceptance Scenarios**:

1. **Given** no existe ninguna materia con el nombre "Bases de Datos",
   **When** el usuario crea una materia con ese nombre,
   **Then** la materia queda creada y visible en el listado de materias.
2. **Given** ya existe una materia llamada "Redes" (en cualquier
   combinación de mayúsculas/minúsculas),
   **When** el usuario intenta crear otra materia llamada "redes",
   **Then** el sistema rechaza la creación y explica que el nombre ya existe.
3. **Given** el usuario está creando una materia,
   **When** deja el nombre vacío e intenta guardar,
   **Then** el sistema rechaza la creación y explica que el nombre es
   obligatorio.

---

### User Story 2 - Editar el nombre de una materia (Priority: P2)

Como usuario, quiero corregir el nombre de una materia existente, para
arreglar errores de tipeo o actualizar el nombre de la asignatura.

**Why this priority**: Valor secundario a crear: importa para mantener el
listado prolijo, pero la app es usable sin esto (se puede recrear la
materia).

**Independent Test**: Se puede probar por completo editando el nombre de una
materia existente y verificando que el cambio se refleja en el listado y en
las tareas/exámenes que ya la referencian.

**Acceptance Scenarios**:

1. **Given** existe una materia llamada "Analisis Matematico",
   **When** el usuario edita su nombre a "Análisis Matemático",
   **Then** el nombre queda actualizado y las tareas/exámenes que ya
   pertenecían a esa materia siguen asociados a ella.
2. **Given** existen las materias "Redes" y "Sistemas Operativos",
   **When** el usuario edita "Sistemas Operativos" para que se llame "redes",
   **Then** el sistema rechaza la edición por nombre duplicado.

---

### User Story 3 - Eliminar una materia (Priority: P3)

Como usuario, quiero eliminar una materia que ya no cursa, para mantener el
listado limpio.

**Why this priority**: Es el caso menos frecuente de los tres — se crean y
editan materias con más frecuencia de la que se eliminan.

**Independent Test**: Se puede probar por completo intentando eliminar una
materia sin tareas/exámenes asociados (debe eliminarse) y una materia con al
menos una tarea o examen asociado (debe bloquearse).

**Acceptance Scenarios**:

1. **Given** una materia sin ninguna tarea ni examen asociado,
   **When** el usuario la elimina,
   **Then** la materia deja de aparecer en el listado.
2. **Given** una materia con al menos una tarea o examen asociado,
   **When** el usuario intenta eliminarla,
   **Then** el sistema bloquea la eliminación y explica que primero debe
   eliminar o reasignar las tareas/exámenes de esa materia.

---

### Edge Cases

Reglas expresadas en formato EARS:

- **Ubicuo**: El sistema SIEMPRE debe considerar dos nombres de materia como
  duplicados si difieren solo en mayúsculas/minúsculas o en espacios al
  inicio/final.
- **Basado en evento**: CUANDO el usuario intenta guardar (crear o editar)
  una materia con el nombre vacío o compuesto solo por espacios, el sistema
  DEBE rechazar la operación e indicar que el nombre es obligatorio.
- **Basado en evento**: CUANDO el usuario intenta guardar una materia con un
  nombre que ya existe, el sistema DEBE rechazar la operación e indicar cuál
  es la materia existente en conflicto.
- **Basado en estado**: MIENTRAS una materia tenga al menos una tarea o
  examen asociado, el sistema DEBE impedir su eliminación.
- **No deseado**: SI el usuario intenta eliminar una materia sin tareas ni
  exámenes asociados, ENTONCES el sistema DEBE eliminarla sin dejar
  referencias huérfanas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to create a new materia providing only a
  name.
- **FR-002**: System MUST reject creating or editing a materia with an empty
  or whitespace-only name.
- **FR-003**: System MUST reject creating or editing a materia whose name
  duplicates an existing materia, comparing case-insensitively and ignoring
  leading/trailing whitespace.
- **FR-004**: Users MUST be able to edit the name of an existing materia.
- **FR-005**: Users MUST be able to view the full list of existing materias.
- **FR-006**: Users MUST be able to delete a materia that has no tareas or
  exámenes associated with it.
- **FR-007**: System MUST prevent deleting a materia that has at least one
  tarea or examen associated, and MUST inform the user of the reason.

### Key Entities *(include if feature involves data)*

- **Materia**: Una asignatura de la facultad a la que pertenecen tareas y
  exámenes (ver `CONTEXT.md`). Se identifica por un nombre único (sin
  distinguir mayúsculas/minúsculas). No tiene más atributos en este MVP.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un usuario puede crear una materia nueva en menos de 10
  segundos desde que abre la pantalla de materias.
- **SC-002**: El 100% de los intentos de crear o editar una materia con
  nombre duplicado son rechazados con un mensaje que identifica el conflicto.
- **SC-003**: El 100% de los intentos de eliminar una materia con
  tareas/exámenes asociados son bloqueados, sin que quede ninguna tarea o
  examen huérfano (sin materia válida) en ningún momento.
- **SC-004**: Un usuario puede encontrar cualquier materia propia en el
  listado sin ayuda externa (listado siempre visible y ordenado).

## Assumptions

- Es una aplicación de un solo usuario por instalación: no hay permisos ni
  roles distintos para gestionar materias.
- El nombre de la materia es texto libre (no existe un catálogo
  predefinido de asignaturas de la facultad).
- No se define una longitud máxima de nombre más allá de un límite
  razonable de interfaz (ej. 100 caracteres), ya que no fue un requisito
  planteado.
