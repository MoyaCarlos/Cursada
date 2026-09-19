# Implementation Plan: Listado de Exámenes por Fecha (HU-08)

**Branch**: `feature/HU-08-listado-examenes-por-fecha` | **Date**: 2026-09-19 | **Spec**: [spec.md](./spec.md)

## Summary

Blindar con un test el orden ascendente por fecha que
`SqliteExamenRepository.listar()` ya implementa desde HU-06. Sin
funcionalidad nueva.

## Technical Context

Sin cambios respecto a HU-07.

## Constitution Check

- ✅ **KISS/YAGNI**: no se toca el SQL existente.

Sin violaciones. Sin `research.md`, `data-model.md` ni `contracts/` —
mismo criterio que HU-05.

## Project Structure

```text
tests/repository/test_sqlite_examen_repository.py   # nuevo
```

## Complexity Tracking

*Sin violaciones.*
