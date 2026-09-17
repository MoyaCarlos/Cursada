from datetime import date

import pytest

from domain.materia import Materia, MateriaInexistenteError
from domain.tarea import Tarea
from services.editar_tarea import EditarTarea
from tests.fakes import MateriaRepositoryFake, TareaRepositoryFake


def test_editar_tarea_guarda_cuando_la_materia_existe():
    materias = MateriaRepositoryFake()
    materia = materias.guardar(Materia(nombre="Bases de Datos"))
    tareas = TareaRepositoryFake()
    tarea = tareas.guardar(
        Tarea(materia_id=materia.id, titulo="TP1", fecha_limite=date(2026, 12, 31))
    )
    servicio = EditarTarea(tareas, materias)

    servicio.ejecutar(
        id=tarea.id,
        materia_id=materia.id,
        titulo="TP1 final",
        fecha_limite=date(2026, 12, 31),
    )

    assert tareas.obtener(tarea.id).titulo == "TP1 final"


def test_editar_tarea_rechaza_materia_inexistente():
    materias = MateriaRepositoryFake()
    materia = materias.guardar(Materia(nombre="Bases de Datos"))
    tareas = TareaRepositoryFake()
    tarea = tareas.guardar(
        Tarea(materia_id=materia.id, titulo="TP1", fecha_limite=date(2026, 12, 31))
    )
    servicio = EditarTarea(tareas, materias)

    with pytest.raises(MateriaInexistenteError):
        servicio.ejecutar(
            id=tarea.id, materia_id=999, titulo="TP1", fecha_limite=date(2026, 12, 31)
        )
