from datetime import date

from domain.materia import Materia
from domain.tarea import Tarea
from repository.db import conectar, crear_tablas
from repository.sqlite_materia_repository import SqliteMateriaRepository
from repository.sqlite_tarea_repository import SqliteTareaRepository


def test_listar_devuelve_las_tareas_ordenadas_por_fecha_limite_ascendente():
    conexion = conectar(":memory:")
    crear_tablas(conexion)
    materias = SqliteMateriaRepository(conexion)
    tareas = SqliteTareaRepository(conexion)
    materia = materias.guardar(Materia(nombre="Bases de Datos"))

    tareas.guardar(
        Tarea(materia_id=materia.id, titulo="Tercera", fecha_limite=date(2026, 12, 31))
    )
    tareas.guardar(
        Tarea(materia_id=materia.id, titulo="Primera", fecha_limite=date(2026, 10, 1))
    )
    tareas.guardar(
        Tarea(materia_id=materia.id, titulo="Segunda", fecha_limite=date(2026, 11, 15))
    )

    titulos = [t.titulo for t in tareas.listar()]

    assert titulos == ["Primera", "Segunda", "Tercera"]
