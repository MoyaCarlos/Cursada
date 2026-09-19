# Feature Specification: Listado de Exámenes por Fecha (HU-08)

**Feature Branch**: `feature/HU-08-listado-examenes-por-fecha`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "HU-08: Ver listado de próximos exámenes ordenado por fecha."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver los exámenes ordenados por fecha (Priority: P1)

Como usuario, quiero ver mis exámenes ordenados del más próximo al más
lejano, para saber cuál rindo primero.

**Why this priority**: Única historia — ya funciona desde HU-06, esta
historia blinda el comportamiento con un test (mismo criterio que HU-05
para tareas).

**Independent Test**: Cargar varios exámenes con fechas distintas, en
cualquier orden, y verificar que el listado los muestra de más próximo a
más lejano.

**Acceptance Scenarios**:

1. **Given** tres exámenes con fechas "2026-12-15", "2026-10-05" y
   "2026-11-20",
   **When** el usuario abre el listado de exámenes,
   **Then** aparecen en el orden "2026-10-05", "2026-11-20", "2026-12-15".

### Edge Cases

- **Ubicuo**: El sistema SIEMPRE ordena el listado de exámenes por fecha
  ascendente, sin importar el orden en que se cargaron.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST list exámenes ordered by fecha ascending
  (soonest first).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de las veces que se abre el listado, los exámenes
  aparecen ordenados por fecha ascendente.

## Assumptions

- El orden ya está implementado desde HU-06 (`ORDER BY eventos.fecha` en
  `SqliteExamenRepository.listar()`); esta historia agrega la cobertura
  de test que faltaba, igual criterio que HU-05 para tareas.
