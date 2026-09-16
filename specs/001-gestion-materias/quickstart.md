# Quickstart: Gestión de Materias (HU-01)

## Prerequisitos

- Python 3.11+.
- **Linux (Arch/CachyOS)**: `sudo pacman -S tk` — necesario para poder abrir
  la ventana. Sin esto, `import tkinter` falla con
  `ImportError: libtk8.6.so: cannot open shared object file`.
- **Windows**: sin pasos extra (el instalador de python.org incluye Tk).

## Instalar dependencias de desarrollo

```bash
pip install pytest pytest-bdd
```

(No hay dependencias de producción fuera de la librería estándar.)

## Correr los tests

```bash
pytest tests/ features/
```

Esperado: todos los tests de dominio (`test_materia.py`), de servicios
(`test_crear_materia.py`, etc.) y el escenario BDD
(`features/gestion_materias.feature`) en verde.

## Ver la app funcionando

```bash
python3 main.py
```

Resultado esperado: se abre una ventana con el listado de materias (vacío la
primera vez), y un formulario para crear una materia nueva. Escenario manual
para validar la historia completa:

1. Crear una materia "Bases de Datos" → aparece en el listado.
2. Intentar crear otra materia "bases de datos" (minúsculas) → se rechaza,
   mensaje de nombre duplicado.
3. Editar "Bases de Datos" a "Bases de Datos II" → el listado se actualiza.
4. Eliminar "Bases de Datos II" (sin tareas/exámenes asociados) → desaparece
   del listado.

La base de datos queda en el directorio de datos de usuario del SO (ver
`research.md`), no en la carpeta del proyecto.
