# Implementation Plan: Listado de Tareas por Fecha Límite (HU-05)

**Branch**: `feature/HU-05-listado-tareas-por-fecha` | **Date**: 2026-09-17 | **Spec**: [spec.md](./spec.md)

## Summary

Agregar el test que falta para blindar el orden ascendente por fecha
límite que `SqliteTareaRepository.listar()` ya implementa desde HU-02
(`ORDER BY eventos.fecha`). No hay funcionalidad nueva.

## Technical Context

Sin cambios respecto a HU-04.

## Constitution Check

- ✅ **KISS/YAGNI**: no se agrega ningún parámetro de ordenamiento
  configurable ni se toca el SQL — ya hace lo que pide la historia.

Sin violaciones. Sin `research.md`, `data-model.md` ni `contracts/`: no hay
ninguna decisión de diseño nueva que documentar ni ningún puerto que
definir — es pura cobertura de test sobre código existente.

## Project Structure

```text
tests/repository/test_sqlite_tarea_repository.py   # nuevo: orden de listar()
```

**Structure Decision**: sin cambios de estructura.

## Complexity Tracking

*Sin violaciones.*
