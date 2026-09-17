from datetime import date

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from domain.materia import Materia
from domain.tarea import MateriaInexistenteError
from services.crear_tarea import CrearTarea
from tests.fakes import MateriaRepositoryFake, TareaRepositoryFake

scenarios("../crear_tarea.feature")


@pytest.fixture
def contexto():
    materias = MateriaRepositoryFake()
    tareas = TareaRepositoryFake()
    return {
        "materias": materias,
        "tareas": tareas,
        "crear_tarea": CrearTarea(tareas, materias),
        "error": None,
    }


def _materia_id(contexto, nombre):
    return next(m.id for m in contexto["materias"].listar() if m.nombre == nombre)


@given(parsers.parse('que existe una materia llamada "{nombre}"'))
def existe_materia(contexto, nombre):
    contexto["materias"].guardar(Materia(nombre=nombre))


@when(
    parsers.parse(
        'el usuario crea una tarea "{titulo}" para "{materia}" con fecha límite "{fecha}"'
    )
)
def crea_tarea(contexto, titulo, materia, fecha):
    contexto["crear_tarea"].ejecutar(
        materia_id=_materia_id(contexto, materia),
        titulo=titulo,
        fecha_limite=date.fromisoformat(fecha),
    )


@when(
    parsers.parse(
        'el usuario intenta crear una tarea sin título para "{materia}" con fecha límite "{fecha}"'
    )
)
def intenta_crear_tarea_sin_titulo(contexto, materia, fecha):
    try:
        contexto["crear_tarea"].ejecutar(
            materia_id=_materia_id(contexto, materia),
            titulo="",
            fecha_limite=date.fromisoformat(fecha),
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse(
        'el usuario intenta crear una tarea "{titulo}" para "{materia}" con fecha límite "{fecha}"'
    )
)
def intenta_crear_tarea_fecha_pasada(contexto, titulo, materia, fecha):
    try:
        contexto["crear_tarea"].ejecutar(
            materia_id=_materia_id(contexto, materia),
            titulo=titulo,
            fecha_limite=date.fromisoformat(fecha),
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse(
        'el usuario intenta crear una tarea "{titulo}" para una materia inexistente '
        'con fecha límite "{fecha}"'
    )
)
def intenta_crear_tarea_materia_inexistente(contexto, titulo, fecha):
    try:
        contexto["crear_tarea"].ejecutar(
            materia_id=999, titulo=titulo, fecha_limite=date.fromisoformat(fecha)
        )
    except MateriaInexistenteError as error:
        contexto["error"] = error


@then(
    parsers.parse(
        'la tarea "{titulo}" aparece en el listado de tareas con estado "{estado}"'
    )
)
def tarea_en_listado(contexto, titulo, estado):
    tarea = next(t for t in contexto["tareas"].listar() if t.titulo == titulo)
    assert tarea.estado.value == estado


@then("el sistema rechaza la creación de la tarea por título obligatorio")
def rechaza_por_titulo(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la creación de la tarea por fecha pasada")
def rechaza_por_fecha(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la creación de la tarea por materia inexistente")
def rechaza_por_materia_inexistente(contexto):
    assert isinstance(contexto["error"], MateriaInexistenteError)
