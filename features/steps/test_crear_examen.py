from datetime import date, time

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from domain.examen import ModalidadExamen
from domain.materia import Materia, MateriaInexistenteError
from services.crear_examen import CrearExamen
from tests.fakes import ExamenRepositoryFake, MateriaRepositoryFake

scenarios("../crear_examen.feature")


@pytest.fixture
def contexto():
    materias = MateriaRepositoryFake()
    examenes = ExamenRepositoryFake()
    return {
        "materias": materias,
        "examenes": examenes,
        "crear_examen": CrearExamen(examenes, materias),
        "error": None,
    }


def _materia_id(contexto, nombre):
    return next(m.id for m in contexto["materias"].listar() if m.nombre == nombre)


@given(parsers.parse('que existe una materia llamada "{nombre}"'))
def existe_materia(contexto, nombre):
    contexto["materias"].guardar(Materia(nombre=nombre))


@when(
    parsers.parse(
        'el usuario crea un examen "{tema}" para "{materia}" el "{fecha}" '
        'a las "{hora}" modalidad "{modalidad}"'
    )
)
def crea_examen(contexto, tema, materia, fecha, hora, modalidad):
    contexto["crear_examen"].ejecutar(
        materia_id=_materia_id(contexto, materia),
        tema=tema,
        fecha=date.fromisoformat(fecha),
        hora=time.fromisoformat(hora),
        modalidad=ModalidadExamen(modalidad),
    )


@when(parsers.parse('el usuario intenta crear un examen sin tema para "{materia}"'))
def intenta_crear_examen_sin_tema(contexto, materia):
    try:
        contexto["crear_examen"].ejecutar(
            materia_id=_materia_id(contexto, materia),
            tema="",
            fecha=date.today(),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse(
        'el usuario intenta crear un examen "{tema}" para "{materia}" el "{fecha}" '
        'a las "{hora}" modalidad "{modalidad}"'
    )
)
def intenta_crear_examen_fecha_pasada(contexto, tema, materia, fecha, hora, modalidad):
    try:
        contexto["crear_examen"].ejecutar(
            materia_id=_materia_id(contexto, materia),
            tema=tema,
            fecha=date.fromisoformat(fecha),
            hora=time.fromisoformat(hora),
            modalidad=ModalidadExamen(modalidad),
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse(
        'el usuario intenta crear un examen "{tema}" para "{materia}" sin indicar hora'
    )
)
def intenta_crear_examen_sin_hora(contexto, tema, materia):
    try:
        contexto["crear_examen"].ejecutar(
            materia_id=_materia_id(contexto, materia),
            tema=tema,
            fecha=date.today(),
            hora=None,
            modalidad=ModalidadExamen.PRESENCIAL,
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse(
        'el usuario intenta crear un examen "{tema}" para "{materia}" sin indicar modalidad'
    )
)
def intenta_crear_examen_sin_modalidad(contexto, tema, materia):
    try:
        contexto["crear_examen"].ejecutar(
            materia_id=_materia_id(contexto, materia),
            tema=tema,
            fecha=date.today(),
            hora=time(14, 0),
            modalidad=None,
        )
    except ValueError as error:
        contexto["error"] = error


@when(
    parsers.parse('el usuario intenta crear un examen "{tema}" para una materia inexistente')
)
def intenta_crear_examen_materia_inexistente(contexto, tema):
    try:
        contexto["crear_examen"].ejecutar(
            materia_id=999,
            tema=tema,
            fecha=date.today(),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
    except MateriaInexistenteError as error:
        contexto["error"] = error


@then(parsers.parse('el examen "{tema}" aparece en el listado de exámenes'))
def examen_en_listado(contexto, tema):
    assert tema in [e.tema for e in contexto["examenes"].listar()]


@then("el sistema rechaza la creación del examen por tema obligatorio")
def rechaza_por_tema(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la creación del examen por fecha pasada")
def rechaza_por_fecha(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la creación del examen por hora obligatoria")
def rechaza_por_hora(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la creación del examen por modalidad obligatoria")
def rechaza_por_modalidad(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], MateriaInexistenteError)


@then("el sistema rechaza la creación del examen por materia inexistente")
def rechaza_por_materia_inexistente(contexto):
    assert isinstance(contexto["error"], MateriaInexistenteError)
