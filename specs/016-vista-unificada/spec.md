# Feature Specification: Ventana Principal con Vista Unificada (HU-16)

**Feature Branch**: `feature/HU-16-vista-unificada`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "HU-16: Ventana principal con vista unificada de \"próximos pendientes\" (tareas + exámenes por fecha)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver tareas y exámenes juntos, ordenados por fecha (Priority: P1)

Como usuario, quiero ver mis tareas y exámenes mezclados en un solo
listado, ordenados por fecha, distinguiendo cuál es cuál y de qué materia
son, para tener de un vistazo todo lo que se me viene sin tener que
revisar dos pantallas separadas.

**Why this priority**: Es el objetivo central de esta historia — es la
razón por la que existe la app (un lugar único para ver los pendientes).

**Independent Test**: Cargar tareas y exámenes de distintas materias con
fechas variadas, abrir la vista unificada, y verificar que aparecen todos
juntos, ordenados por fecha, cada uno indicando su tipo y su materia.

**Acceptance Scenarios**:

1. **Given** existen tareas y exámenes de varias materias con fechas
   distintas,
   **When** el usuario abre la vista de pendientes,
   **Then** ve un único listado con todos, ordenados de fecha más próxima
   a más lejana, cada fila indicando si es tarea o examen, su materia y
   su fecha.
2. **Given** una tarea y un examen tienen la misma fecha,
   **When** el usuario abre el listado,
   **Then** ambos aparecen (el orden entre ellos no está definido).
3. **Given** no hay ninguna tarea ni examen cargado,
   **When** el usuario abre la vista de pendientes,
   **Then** ve el listado vacío, sin error.

---

### User Story 2 - Una sola ventana con las distintas pantallas como pestañas (Priority: P2)

Como usuario, quiero que la app se abra en una sola ventana con pestañas
(Pendientes, Materias, Tareas, Exámenes) en vez de varias ventanas
sueltas, para que sea más cómoda de usar.

**Why this priority**: Es una mejora de usabilidad sobre lo ya construido
en HU-01/02/06 (que abrían 3 ventanas independientes) — depende de que
"Pendientes" (US1) exista para tener sentido como primera pestaña.

**Independent Test**: Abrir la app y verificar que aparece una sola
ventana con 4 pestañas, y que crear una materia en la pestaña Materias
hace que aparezca disponible para elegir en las pestañas Tareas/Exámenes
al pasar a ellas.

**Acceptance Scenarios**:

1. **Given** el usuario abre la aplicación,
   **When** se inicia,
   **Then** aparece una sola ventana con 4 pestañas: Pendientes, Materias,
   Tareas, Exámenes.
2. **Given** el usuario crea una materia nueva en la pestaña Materias,
   **When** cambia a la pestaña Tareas o Exámenes,
   **Then** la materia nueva está disponible para elegir.
3. **Given** el usuario crea o edita una tarea/examen,
   **When** vuelve a la pestaña Pendientes,
   **Then** el cambio se refleja en la vista unificada.

---

### Edge Cases

- **Ubicuo**: El listado de pendientes SIEMPRE combina tareas y exámenes
  en un único orden por fecha ascendente.
- **Basado en evento**: CUANDO el usuario cambia de pestaña, el sistema
  DEBE refrescar los datos de esa pestaña (materias disponibles,
  listado), para que nunca muestre información desactualizada.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST show tareas and exámenes together in one list,
  ordered by date ascending.
- **FR-002**: Each row in the unified list MUST indicate whether it is a
  tarea or an examen, its materia, and its date.
- **FR-003**: The application MUST open as a single window with tabs for
  Pendientes, Materias, Tareas and Exámenes, replacing the previous
  separate windows.
- **FR-004**: Switching to a tab MUST refresh that tab's data (materias
  available, items listed).

### Key Entities

- **Ítem pendiente**: una proyección de solo lectura para esta vista —
  no es una entidad de dominio nueva (`Evento` sigue sin existir como
  clase, ver `CONTEXT.md`); se arma combinando `Tarea` y `Examen` ya
  existentes, solo para mostrarlos juntos.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de las tareas y exámenes cargados aparecen en la
  vista de pendientes, sin duplicados ni faltantes.
- **SC-002**: Un usuario puede ver todo lo que tiene pendiente sin
  cambiar de ventana (una sola ventana para toda la app).

## Assumptions

- La vista de pendientes es de solo lectura en esta historia — crear,
  editar, eliminar o cambiar estado se sigue haciendo desde las pestañas
  de Tareas/Exámenes (ya construidas). Combinar esas acciones en la vista
  unificada, si hiciera falta, sería una historia aparte.
- No se filtra por estado/materia/fecha en esta vista — eso es HU-22
  (filtros), historia aparte y posterior. Acá se muestran todos los
  pendientes sin excepción, igual criterio ya aplicado en HU-05/HU-08.
- No se distingue "completado"/"vencido" visualmente en esta vista más
  allá del estado que ya se muestra para tareas — la regla de
  "completado" para exámenes (inferida por fecha, ver
  `docs/modelo-datos.md`) se usa recién cuando HU-22 filtre por ese
  criterio.
