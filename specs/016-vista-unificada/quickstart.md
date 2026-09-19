# Quickstart: Ventana Principal con Vista Unificada (HU-16)

```bash
.venv/bin/python -m pytest -q
.venv/bin/python main.py
```

Escenario manual:

1. Abrir la app → debe aparecer **una sola ventana** con 4 pestañas:
   Pendientes, Materias, Tareas, Exámenes.
2. En Materias, crear una materia nueva.
3. Ir a la pestaña Tareas → la materia nueva debe estar disponible en el
   combo sin reiniciar la app.
4. Crear una tarea y un examen de fechas distintas para esa materia.
5. Ir a la pestaña Pendientes → deben aparecer ambos juntos, ordenados
   por fecha, cada uno indicando si es tarea o examen y su materia.
6. Sin ninguna tarea/examen cargado (probar con una DB nueva): la pestaña
   Pendientes debe mostrarse vacía, sin error.
