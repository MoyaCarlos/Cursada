# Quickstart: Crear Examen (HU-06)

```bash
.venv/bin/python -m pytest -q
.venv/bin/python main.py
```

Escenario manual:

1. Crear una materia (si no hay ninguna).
2. Abrir la ventana de exámenes, completar materia, tema, fecha, hora y
   modalidad (notas opcional) → aparece en el listado.
3. Tema vacío → rechazo.
4. Fecha de ayer → rechazo.
5. Sin hora → rechazo.
6. Sin elegir modalidad → rechazo.
