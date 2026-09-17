# Quickstart: Editar/Eliminar Tarea (HU-03)

```bash
.venv/bin/python -m pytest -q
.venv/bin/python main.py
```

Escenario manual:

1. Crear una tarea, seleccionarla en el listado y editarle el título →
   se refleja en el listado.
2. Editar una tarea a título vacío → se rechaza.
3. Editar la fecha límite de una tarea a una fecha pasada → se rechaza.
4. Crear una tarea con fecha de hoy, esperar (o simular) que quede vencida,
   y editar solo la descripción sin tocar la fecha → debe permitirlo.
5. Eliminar una tarea → desaparece del listado.
