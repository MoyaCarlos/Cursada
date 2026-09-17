from datetime import date, timedelta

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from domain.materia import Materia
from domain.tarea import MateriaInexistenteError, Tarea
from services.editar_tarea import EditarTarea
from services.eliminar_tarea import EliminarTarea
from tests.fakes import MateriaRepositoryFake, TareaRepositoryFake

scenarios("../editar_eliminar_tarea.feature")


@pytest.fixture
def contexto():
    materias = MateriaRepositoryFake()
    tareas = TareaRepositoryFake()
    return {
        "materias": materias,
        "tareas": tareas,
        "editar": EditarTarea(tareas, materias),
        "eliminar": EliminarTarea(tareas),
        "error": None,
    }


def _materia_id(contexto, nombre):
    return next(m.id for m in contexto["materias"].listar() if m.nombre == nombre)


def _tarea_por_titulo(contexto, titulo):
    return next(t for t in contexto["tareas"].listar() if t.titulo == titulo)


@given(parsers.parse('que existe una materia llamada "{nombre}"'))
def existe_materia(contexto, nombre):
    contexto["materias"].guardar(Materia(nombre=nombre))


@given(
    parsers.parse(
        'que existe una tarea "{titulo}" para "{materia}" con fecha límite "{fecha}"'
    )
)
def existe_tarea(contexto, titulo, materia, fecha):
    contexto["tareas"].guardar(
        Tarea(
            materia_id=_materia_id(contexto, materia),
            titulo=titulo,
            fecha_limite=date.fromisoformat(fecha),
        )
    )


@given(parsers.parse('que existe una tarea vencida "{titulo}" para "{materia}"'))
def existe_tarea_vencida(contexto, titulo, materia):
    vencida = date.today() - timedelta(days=5)
    contexto["tareas"].guardar(
        Tarea(
            materia_id=_materia_id(contexto, materia), titulo=titulo, fecha_limite=vencida
        )
    )


@when(parsers.parse('el usuario edita el título de "{titulo_actual}" a "{titulo_nuevo}"'))
def edita_titulo(contexto, titulo_actual, titulo_nuevo):
    tarea = _tarea_por_titulo(contexto, titulo_actual)
    contexto["editar"].ejecutar(
        id=tarea.id,
        materia_id=tarea.materia_id,
        titulo=titulo_nuevo,
        fecha_limite=tarea.fecha_limite,
    )


@when(parsers.parse('el usuario intenta editar el título de "{titulo_actual}" dejándolo vacío'))
def intenta_editar_titulo_vacio(contexto, titulo_actual):
    tarea = _tarea_por_titulo(contexto, titulo_actual)
    try:
        contexto["editar"].ejecutar(
            id=tarea.id,
            materia_id=tarea.materia_id,
            titulo="",
            fecha_limite=tarea.fecha_limite,
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse('el usuario intenta cambiar la fecha límite de "{titulo}" a "{fecha}"')
)
def intenta_cambiar_fecha(contexto, titulo, fecha):
    tarea = _tarea_por_titulo(contexto, titulo)
    try:
        contexto["editar"].ejecutar(
            id=tarea.id,
            materia_id=tarea.materia_id,
            titulo=tarea.titulo,
            fecha_limite=date.fromisoformat(fecha),
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse(
        'el usuario edita la descripción de "{titulo}" a "{descripcion}" sin cambiar la fecha'
    )
)
def edita_descripcion_sin_cambiar_fecha(contexto, titulo, descripcion):
    tarea = _tarea_por_titulo(contexto, titulo)
    contexto["editar"].ejecutar(
        id=tarea.id,
        materia_id=tarea.materia_id,
        titulo=tarea.titulo,
        fecha_limite=tarea.fecha_limite,
        descripcion=descripcion,
    )


@when(parsers.parse('el usuario intenta reasignar "{titulo}" a una materia inexistente'))
def intenta_reasignar_materia_inexistente(contexto, titulo):
    tarea = _tarea_por_titulo(contexto, titulo)
    try:
        contexto["editar"].ejecutar(
            id=tarea.id,
            materia_id=999,
            titulo=tarea.titulo,
            fecha_limite=tarea.fecha_limite,
        )
    except MateriaInexistenteError as error:
        contexto["error"] = error


@when(parsers.parse('el usuario elimina la tarea "{titulo}"'))
def elimina_tarea(contexto, titulo):
    tarea = _tarea_por_titulo(contexto, titulo)
    contexto["eliminar"].ejecutar(tarea.id)


@then(parsers.parse('la tarea "{titulo}" aparece en el listado de tareas'))
def tarea_en_listado(contexto, titulo):
    assert titulo in [t.titulo for t in contexto["tareas"].listar()]


@then(parsers.parse('la tarea "{titulo}" no aparece en el listado de tareas'))
def tarea_no_en_listado(contexto, titulo):
    assert titulo not in [t.titulo for t in contexto["tareas"].listar()]


@then(parsers.parse('la tarea "{titulo}" conserva su fecha límite original'))
def tarea_conserva_fecha(contexto, titulo):
    tarea = _tarea_por_titulo(contexto, titulo)
    assert tarea.fecha_limite < date.today()
    assert tarea.descripcion == "actualizada"


@then("el sistema rechaza la edición de la tarea por título obligatorio")
def rechaza_por_titulo(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la edición de la tarea por fecha pasada")
def rechaza_por_fecha(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la edición de la tarea por materia inexistente")
def rechaza_por_materia_inexistente(contexto):
    assert isinstance(contexto["error"], MateriaInexistenteError)
