# Implementation Plan: Ventana Principal con Vista Unificada (HU-16)

**Branch**: `feature/HU-16-vista-unificada` | **Date**: 2026-09-19 | **Spec**: [spec.md](./spec.md)

## Summary

Agregar un servicio que combina tareas y exámenes en un único listado
ordenado por fecha (US1), y consolidar las 3 ventanas sueltas
(`VentanaMaterias`, `VentanaTareas`, `VentanaExamenes`) en una sola
ventana con pestañas, agregando una cuarta pestaña "Pendientes" (US2).

## Technical Context

Sin cambios de stack. No se agregan tablas ni columnas — se reutilizan
`TareaRepository.listar()`, `ExamenRepository.listar()` y
`MateriaRepository.listar()` tal cual existen.

## Constitution Check

- ✅ **KISS/YAGNI**: no se crea una clase `Evento` de dominio (ver
  `research.md`); el listado combinado es una proyección de solo lectura
  en la capa de `services/`, no una entidad nueva.
- ✅ **DRY**: el listado unificado reutiliza `listar()` de los 3
  repositorios existentes — no se agrega SQL nuevo.
- ✅ **SOLID (SRP)**: `ListarPendientes` es un service dedicado a este
  único caso de uso, igual criterio que el resto.

Sin violaciones.

## Project Structure

### Documentation (this feature)

```text
specs/016-vista-unificada/
├── plan.md / research.md / data-model.md / quickstart.md
└── tasks.md
```

### Source Code

```text
services/listar_pendientes.py     # nuevo: ItemPendiente + ListarPendientes

ui/ventana_materias.py            # VentanaMaterias(tk.Tk) -> PanelMaterias(ttk.Frame)
ui/ventana_tareas.py              # VentanaTareas(tk.Toplevel) -> PanelTareas(ttk.Frame)
ui/ventana_examenes.py            # VentanaExamenes(tk.Toplevel) -> PanelExamenes(ttk.Frame)
ui/panel_pendientes.py            # nuevo: PanelPendientes(ttk.Frame)
ui/ventana_principal.py           # nuevo: tk.Tk + ttk.Notebook con las 4 pestañas
main.py                           # wiring actualizado a VentanaPrincipal

tests/services/test_listar_pendientes.py   # nuevo
```

**Structure Decision**: se renombran los tres módulos de ventana
existentes a paneles (mismo archivo, misma lógica interna de negocio sin
cambios — solo la clase base de Tkinter cambia de `Tk`/`Toplevel` a
`Frame` y se quitan `title()`/`geometry()`). Ningún test automatizado
depende de esos nombres de clase (se verificó con grep antes de
arrancar), así que el renombre no rompe la suite.

## Complexity Tracking

*Sin violaciones.*
