import pytest

from domain.materia import Materia, NombreDuplicadoError
from services.crear_materia import CrearMateria
from tests.fakes import MateriaRepositoryFake


def test_crear_materia_guarda_cuando_el_nombre_no_existe():
    repositorio = MateriaRepositoryFake()
    servicio = CrearMateria(repositorio)

    materia = servicio.ejecutar("Bases de Datos")

    assert materia.id is not None
    assert [m.nombre for m in repositorio.listar()] == ["Bases de Datos"]


def test_crear_materia_rechaza_nombre_duplicado_case_insensitive():
    repositorio = MateriaRepositoryFake()
    repositorio.guardar(Materia(nombre="Redes"))
    servicio = CrearMateria(repositorio)

    with pytest.raises(NombreDuplicadoError):
        servicio.ejecutar("redes")
