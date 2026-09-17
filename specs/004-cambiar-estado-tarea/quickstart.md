# Quickstart: Cambiar Estado de una Tarea (HU-04)

```bash
.venv/bin/python -m pytest -q
.venv/bin/python main.py
```

Escenario manual:

1. Crear una tarea (nace "pendiente").
2. Seleccionarla, elegir "en_progreso" en el combo de estado, tocar
   "Cambiar estado" → el listado la muestra "en_progreso".
3. Cambiarla a "completada" → se refleja.
4. Cambiarla de vuelta a "pendiente" → se permite sin problema.
5. Sin seleccionar ninguna tarea, tocar "Cambiar estado" → avisa que hay
   que seleccionar una.
