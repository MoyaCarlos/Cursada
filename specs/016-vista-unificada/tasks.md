# Tasks: Ventana Principal con Vista Unificada (HU-16)

## Phase 1: Setup
Ninguno nuevo.

## Phase 2: Foundational
Ninguno — US1 y US2 no comparten prerequisito bloqueante más allá de lo
que ya existe.

---

## Phase 3: User Story 1 - Listado unificado por fecha (Priority: P1) 🎯 MVP

### Tests

- [ ] T001 [P] [US1] `tests/services/test_listar_pendientes.py`:
  `ListarPendientes` combina tareas y exámenes de varias materias,
  ordenados por fecha ascendente (usando `time.min` para tareas al
  comparar con exámenes que sí tienen hora); devuelve lista vacía sin
  tareas ni exámenes.

### Implementation

- [ ] T002 [US1] Crear `services/listar_pendientes.py` con el dataclass
  `ItemPendiente` y la clase `ListarPendientes` (ver `data-model.md`).
- [ ] T003 [US1] Crear `ui/panel_pendientes.py` (`PanelPendientes`,
  `ttk.Frame`): listado de solo lectura mostrando tipo, materia, título y
  fecha (y hora si es examen); método público `actualizar()`.

**Checkpoint**: el servicio y el panel de solo lectura funcionan.

---

## Phase 4: User Story 2 - Consolidar en una ventana con pestañas (Priority: P2)

### Implementation
*(sin tests nuevos — es un refactor de UI sobre código ya cubierto por
los tests de HU-01/02/03/04/06/07; se verifica con `quickstart.md`)*

- [ ] T004 [US2] En `ui/ventana_materias.py`: renombrar
  `VentanaMaterias(tk.Tk)` a `PanelMaterias(ttk.Frame)`; quitar
  `title()`/`geometry()`; agregar método público `actualizar()` (llama a
  `_refrescar_listado()`).
- [ ] T005 [US2] En `ui/ventana_tareas.py`: renombrar
  `VentanaTareas(tk.Toplevel)` a `PanelTareas(ttk.Frame)`; recibir el
  repositorio de materias por parámetro igual que antes; agregar
  `actualizar()` (llama a `_refrescar_materias()` y
  `_refrescar_listado()`).
- [ ] T006 [US2] En `ui/ventana_examenes.py`: mismo tratamiento →
  `PanelExamenes(ttk.Frame)` con `actualizar()`.
- [ ] T007 [US2] Crear `ui/ventana_principal.py`: `VentanaPrincipal(tk.Tk)`
  con un `ttk.Notebook` de 4 pestañas (Pendientes, Materias, Tareas,
  Exámenes) construidas con los repositorios ya wireados; se suscribe a
  `<<NotebookTabChanged>>` para llamar `actualizar()` del panel que pasa
  a estar visible.
- [ ] T008 [US2] Actualizar `main.py` para instanciar `VentanaPrincipal`
  en vez de las 3 ventanas sueltas.

**Checkpoint**: una sola ventana, 4 pestañas, refresco correcto al
cambiar de pestaña.

---

## Phase 5: Polish

- [ ] T009 [P] Correr `quickstart.md` a mano (los 6 pasos, con especial
  atención al refresco de materias al cambiar de pestaña).
- [ ] T010 Revisar el diff completo antes de mergear.
- [ ] T011 Marcar HU-16 como completada en `docs/backlog.md`.
