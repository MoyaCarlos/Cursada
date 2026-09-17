# Quickstart: Crear Tarea Pendiente (HU-02)

## Prerequisitos

Los mismos que HU-01 (venv con `pytest`/`pytest-bdd`, `tk` instalado en
Linux). Nada nuevo.

## Correr los tests

```bash
.venv/bin/python -m pytest -q
```

## Ver la app funcionando

```bash
.venv/bin/python main.py
```

Escenario manual:

1. Crear al menos una materia (si no hay ninguna, la ventana de tareas debe
   avisar que hace falta una materia antes de cargar una tarea).
2. Abrir la ventana de tareas, elegir la materia, completar título, fecha
   límite y prioridad (descripción es opcional) → la tarea aparece en el
   listado con estado "pendiente".
3. Intentar crear una tarea con título vacío → se rechaza.
4. Intentar crear una tarea con fecha límite de ayer → se rechaza.
