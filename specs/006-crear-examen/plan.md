# Implementation Plan: Crear Examen (HU-06)

**Branch**: `feature/HU-06-crear-examen` | **Date**: 2026-09-17 | **Spec**: [spec.md](./spec.md)

## Summary

Permitir crear un examen (materia, tema, fecha, hora, modalidad, notas
opcionales), reutilizando el patrón ya establecido para tareas (HU-02),
adaptado a los campos propios de un examen.

## Technical Context

Sin cambios de stack respecto a HU-05. Se agregan las tablas `modalidades`
(lookup, ya diseñada en `docs/modelo-datos.md`, todavía no creada en
`db.py`) y `examenes`.

## Constitution Check

- ✅ **DRY**: `MateriaInexistenteError` se reubica de `domain/tarea.py` a
  `domain/materia.py` (ver `research.md`) — ahora la usan tanto `Tarea`
  como `Examen`, y vivía en el lugar equivocado.
- ✅ **KISS**: mismo patrón que `Tarea` (dataclass plano, sin clase
  `Evento`); `hora`/`modalidad` obligatorios se validan con `None` como
  sentinel de "no elegido", igual que se valida `titulo` vacío en tareas.
- ✅ **YAGNI**: sin editar/eliminar examen (HU-07, aparte); sin listado
  unificado con tareas (HU-16, aparte).
- ✅ **Repository / Factory function**: mismos patrones, sin novedad.

Sin violaciones.

## Project Structure

### Documentation (this feature)

```text
specs/006-crear-examen/
├── plan.md / research.md / data-model.md / quickstart.md
├── contracts/examen_repository.md
└── tasks.md
```

### Source Code

```text
domain/materia.py            # + MateriaInexistenteError (reubicado desde tarea.py)
domain/tarea.py               # - MateriaInexistenteError (ahora importa de materia.py)
domain/examen.py              # nuevo: ModalidadExamen, Examen, crear_examen()
repository/db.py                          # + tablas modalidades, examenes
repository/examen_repository.py           # nuevo: Protocol
repository/sqlite_examen_repository.py    # nuevo
services/crear_examen.py                  # nuevo
ui/ventana_examenes.py                    # nuevo
main.py                                   # + wiring de exámenes
tests/domain/test_examen.py               # nuevo
tests/services/test_crear_examen.py       # nuevo
tests/fakes.py                            # + ExamenRepositoryFake
features/crear_examen.feature             # nuevo
```

**Structure Decision**: mismo proyecto único.

## Complexity Tracking

*Sin violaciones.*
