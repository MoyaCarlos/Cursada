# Feature Specification: Listado de Tareas por Fecha Límite (HU-05)

**Feature Branch**: `feature/HU-05-listado-tareas-por-fecha`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User description: "HU-05: Ver listado de tareas pendientes ordenado por fecha límite."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver las tareas ordenadas por fecha límite (Priority: P1)

Como usuario, quiero ver mis tareas ordenadas de la más próxima a vencer a
la más lejana, para saber qué tengo que atender primero.

**Why this priority**: Es la única historia de esta feature — ya venía
funcionando desde HU-02/HU-03/HU-04, esta historia formaliza y blinda con
un test el comportamiento.

**Independent Test**: Cargar varias tareas con fechas límite distintas, en
cualquier orden, y verificar que el listado las muestra ordenadas de fecha
más próxima a más lejana.

**Acceptance Scenarios**:

1. **Given** tres tareas con fechas límite "2026-12-31", "2026-10-01" y
   "2026-11-15",
   **When** el usuario abre el listado de tareas,
   **Then** aparecen en el orden "2026-10-01", "2026-11-15", "2026-12-31".
2. **Given** dos tareas con la misma fecha límite,
   **When** el usuario abre el listado,
   **Then** ambas aparecen (el orden entre ellas no está definido, no es un
   requisito de esta historia).

---

### Edge Cases

- **Ubicuo**: El sistema SIEMPRE ordena el listado de tareas por fecha
  límite ascendente (la más próxima primero), sin importar el orden en que
  se cargaron.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST list tareas ordered by fecha límite ascending
  (soonest first).

### Key Entities

- **Tarea**: sin cambios — esta historia verifica el orden de `listar()`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de las veces que se abre el listado, las tareas
  aparecen ordenadas por fecha límite ascendente.

## Assumptions

- "Tareas pendientes" en el nombre de la historia se interpreta como "el
  listado de tareas en general" (lo que ya muestra `ventana_tareas.py`,
  con su estado visible), no como un filtro exclusivo al estado
  "pendiente" — ese filtro específico es HU-22 (filtros por estado,
  materia y fecha), una historia aparte y posterior en el backlog.
- El orden ya está implementado desde HU-02 (`ORDER BY eventos.fecha` en
  `SqliteTareaRepository.listar()`); esta historia agrega la cobertura de
  test que faltaba para blindar ese comportamiento.
