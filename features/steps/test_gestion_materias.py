import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from domain.materia import Materia, NombreDuplicadoError
from services.crear_materia import CrearMateria
from services.editar_materia import EditarMateria
from tests.fakes import MateriaRepositoryFake

scenarios("../gestion_materias.feature")


@pytest.fixture
def contexto():
    repositorio = MateriaRepositoryFake()
    return {
        "repositorio": repositorio,
        "crear": CrearMateria(repositorio),
        "editar": EditarMateria(repositorio),
        "error": None,
    }


def _materia_por_nombre(contexto, nombre):
    return next(m for m in contexto["repositorio"].listar() if m.nombre == nombre)


@given(parsers.parse('que no existe ninguna materia llamada "{nombre}"'))
def no_existe_materia(contexto, nombre):
    assert contexto["repositorio"].existe_nombre(nombre) is False


@given(parsers.parse('que existe una materia llamada "{nombre}"'))
def existe_materia(contexto, nombre):
    contexto["repositorio"].guardar(Materia(nombre=nombre))


@when(parsers.parse('el usuario crea una materia llamada "{nombre}"'))
def crea_materia(contexto, nombre):
    contexto["crear"].ejecutar(nombre)


@when(parsers.parse('el usuario intenta crear una materia llamada "{nombre}"'))
def intenta_crear_materia(contexto, nombre):
    try:
        contexto["crear"].ejecutar(nombre)
    except NombreDuplicadoError as error:
        contexto["error"] = error


@when("el usuario intenta crear una materia con nombre vacío")
def intenta_crear_materia_vacia(contexto):
    try:
        contexto["crear"].ejecutar("")
    except ValueError as error:
        contexto["error"] = error


@when(parsers.parse('el usuario edita "{nombre_actual}" para que se llame "{nombre_nuevo}"'))
def edita_materia(contexto, nombre_actual, nombre_nuevo):
    materia = _materia_por_nombre(contexto, nombre_actual)
    contexto["editar"].ejecutar(materia.id, nombre_nuevo)


@when(
    parsers.parse(
        'el usuario intenta editar "{nombre_actual}" para que se llame "{nombre_nuevo}"'
    )
)
def intenta_editar_materia(contexto, nombre_actual, nombre_nuevo):
    materia = _materia_por_nombre(contexto, nombre_actual)
    try:
        contexto["editar"].ejecutar(materia.id, nombre_nuevo)
    except NombreDuplicadoError as error:
        contexto["error"] = error


@then(parsers.parse('la materia "{nombre}" aparece en el listado de materias'))
def materia_en_listado(contexto, nombre):
    assert nombre in [m.nombre for m in contexto["repositorio"].listar()]


@then("el sistema rechaza la creación por nombre duplicado")
def rechaza_creacion_por_duplicado(contexto):
    assert isinstance(contexto["error"], NombreDuplicadoError)


@then("el sistema rechaza la creación por nombre obligatorio")
def rechaza_por_nombre_obligatorio(contexto):
    assert isinstance(contexto["error"], ValueError)
    assert not isinstance(contexto["error"], NombreDuplicadoError)


@then("el sistema rechaza la edición por nombre duplicado")
def rechaza_edicion_por_duplicado(contexto):
    assert isinstance(contexto["error"], NombreDuplicadoError)
