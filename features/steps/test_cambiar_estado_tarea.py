from datetime import date

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from domain.tarea import EstadoTarea, Tarea
from services.cambiar_estado_tarea import CambiarEstadoTarea
from tests.fakes import TareaRepositoryFake

scenarios("../cambiar_estado_tarea.feature")


@pytest.fixture
def contexto():
    tareas = TareaRepositoryFake()
    return {"tareas": tareas, "servicio": CambiarEstadoTarea(tareas)}


def _tarea_por_titulo(contexto, titulo):
    return next(t for t in contexto["tareas"].listar() if t.titulo == titulo)


@given(parsers.parse('que existe una tarea "{titulo}" con estado "{estado}"'))
def existe_tarea_con_estado(contexto, titulo, estado):
    contexto["tareas"].guardar(
        Tarea(
            materia_id=1,
            titulo=titulo,
            fecha_limite=date(2026, 12, 31),
            estado=EstadoTarea(estado),
        )
    )


@when(parsers.parse('el usuario cambia el estado de "{titulo}" a "{nuevo_estado}"'))
def cambia_estado(contexto, titulo, nuevo_estado):
    tarea = _tarea_por_titulo(contexto, titulo)
    contexto["servicio"].ejecutar(id=tarea.id, nuevo_estado=EstadoTarea(nuevo_estado))


@then(parsers.parse('la tarea "{titulo}" tiene estado "{estado}"'))
def tarea_tiene_estado(contexto, titulo, estado):
    tarea = _tarea_por_titulo(contexto, titulo)
    assert tarea.estado == EstadoTarea(estado)
