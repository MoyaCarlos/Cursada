from datetime import date, time

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from domain.examen import Examen, ModalidadExamen
from domain.materia import Materia, MateriaInexistenteError
from services.editar_examen import EditarExamen
from services.eliminar_examen import EliminarExamen
from tests.fakes import ExamenRepositoryFake, MateriaRepositoryFake

scenarios("../editar_eliminar_examen.feature")


@pytest.fixture
def contexto():
    materias = MateriaRepositoryFake()
    examenes = ExamenRepositoryFake()
    return {
        "materias": materias,
        "examenes": examenes,
        "editar": EditarExamen(examenes, materias),
        "eliminar": EliminarExamen(examenes),
        "error": None,
    }


def _materia_id(contexto, nombre):
    return next(m.id for m in contexto["materias"].listar() if m.nombre == nombre)


def _examen_por_tema(contexto, tema):
    return next(e for e in contexto["examenes"].listar() if e.tema == tema)


@given(parsers.parse('que existe una materia llamada "{nombre}"'))
def existe_materia(contexto, nombre):
    contexto["materias"].guardar(Materia(nombre=nombre))


@given(
    parsers.parse(
        'que existe un examen "{tema}" para "{materia}" el "{fecha}" '
        'a las "{hora}" modalidad "{modalidad}"'
    )
)
def existe_examen(contexto, tema, materia, fecha, hora, modalidad):
    contexto["examenes"].guardar(
        Examen(
            materia_id=_materia_id(contexto, materia),
            tema=tema,
            fecha=date.fromisoformat(fecha),
            hora=time.fromisoformat(hora),
            modalidad=ModalidadExamen(modalidad),
        )
    )


@when(parsers.parse('el usuario edita el tema de "{tema_actual}" a "{tema_nuevo}"'))
def edita_tema(contexto, tema_actual, tema_nuevo):
    examen = _examen_por_tema(contexto, tema_actual)
    contexto["editar"].ejecutar(
        id=examen.id,
        materia_id=examen.materia_id,
        tema=tema_nuevo,
        fecha=examen.fecha,
        hora=examen.hora,
        modalidad=examen.modalidad,
    )


@when(parsers.parse('el usuario intenta editar el tema de "{tema_actual}" dejándolo vacío'))
def intenta_editar_tema_vacio(contexto, tema_actual):
    examen = _examen_por_tema(contexto, tema_actual)
    try:
        contexto["editar"].ejecutar(
            id=examen.id,
            materia_id=examen.materia_id,
            tema="",
            fecha=examen.fecha,
            hora=examen.hora,
            modalidad=examen.modalidad,
        )
    except ValueError as error:
        contexto["error"] = error


@when(parsers.parse('el usuario intenta cambiar la fecha de "{tema}" a "{fecha}"'))
def intenta_cambiar_fecha(contexto, tema, fecha):
    examen = _examen_por_tema(contexto, tema)
    try:
        contexto["editar"].ejecutar(
            id=examen.id,
            materia_id=examen.materia_id,
            tema=examen.tema,
            fecha=date.fromisoformat(fecha),
            hora=examen.hora,
            modalidad=examen.modalidad,
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse(
        'el usuario intenta reasignar el examen "{tema}" a una materia inexistente'
    )
)
def intenta_reasignar_materia_inexistente(contexto, tema):
    examen = _examen_por_tema(contexto, tema)
    try:
        contexto["editar"].ejecutar(
            id=examen.id,
            materia_id=999,
            tema=examen.tema,
            fecha=examen.fecha,
            hora=examen.hora,
            modalidad=examen.modalidad,
        )
    except MateriaInexistenteError as error:
        contexto["error"] = error


@when(parsers.parse('el usuario elimina el examen "{tema}"'))
def elimina_examen(contexto, tema):
    examen = _examen_por_tema(contexto, tema)
    contexto["eliminar"].ejecutar(examen.id)


@then(parsers.parse('el examen "{tema}" aparece en el listado de exámenes'))
def examen_en_listado(contexto, tema):
    assert tema in [e.tema for e in contexto["examenes"].listar()]


@then(parsers.parse('el examen "{tema}" no aparece en el listado de exámenes'))
def examen_no_en_listado(contexto, tema):
    assert tema not in [e.tema for e in contexto["examenes"].listar()]


@then("el sistema rechaza la edición del examen por tema obligatorio")
def rechaza_por_tema(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la edición del examen por fecha pasada")
def rechaza_por_fecha(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la edición del examen por materia inexistente")
def rechaza_por_materia_inexistente(contexto):
    assert isinstance(contexto["error"], MateriaInexistenteError)
