# Quickstart: Editar/Eliminar Examen (HU-07)

```bash
.venv/bin/python -m pytest -q
.venv/bin/python main.py
```

Escenario manual:

1. Crear un examen, seleccionarlo y editarle el tema → se refleja.
2. Editar dejando tema/hora vacíos o sin modalidad → rechazo.
3. Cambiar la fecha a una pasada → rechazo; sin tocar la fecha de un
   examen ya vencido → permitido.
4. Eliminar un examen → desaparece del listado.
