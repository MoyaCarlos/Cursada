from datetime import date

import pytest

from domain.materia import Materia
from domain.tarea import MateriaInexistenteError
from services.crear_tarea import CrearTarea
from tests.fakes import MateriaRepositoryFake, TareaRepositoryFake


def test_crear_tarea_guarda_cuando_la_materia_existe():
    materias = MateriaRepositoryFake()
    materia = materias.guardar(Materia(nombre="Bases de Datos"))
    tareas = TareaRepositoryFake()
    servicio = CrearTarea(tareas, materias)

    tarea = servicio.ejecutar(
        materia_id=materia.id, titulo="TP1", fecha_limite=date(2026, 12, 31)
    )

    assert tarea.id is not None
    assert [t.titulo for t in tareas.listar()] == ["TP1"]


def test_crear_tarea_rechaza_materia_inexistente():
    materias = MateriaRepositoryFake()
    tareas = TareaRepositoryFake()
    servicio = CrearTarea(tareas, materias)

    with pytest.raises(MateriaInexistenteError):
        servicio.ejecutar(materia_id=999, titulo="TP1", fecha_limite=date(2026, 12, 31))

    assert tareas.listar() == []
