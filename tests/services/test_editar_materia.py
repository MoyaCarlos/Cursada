import pytest

from domain.materia import Materia, NombreDuplicadoError
from services.editar_materia import EditarMateria
from tests.fakes import MateriaRepositoryFake


def test_editar_materia_actualiza_el_nombre():
    repositorio = MateriaRepositoryFake()
    materia = repositorio.guardar(Materia(nombre="Analisis Matematico"))
    servicio = EditarMateria(repositorio)

    servicio.ejecutar(materia.id, "Análisis Matemático")

    assert repositorio.obtener(materia.id).nombre == "Análisis Matemático"


def test_editar_materia_rechaza_nombre_usado_por_otra_materia():
    repositorio = MateriaRepositoryFake()
    repositorio.guardar(Materia(nombre="Redes"))
    materia_b = repositorio.guardar(Materia(nombre="Sistemas Operativos"))
    servicio = EditarMateria(repositorio)

    with pytest.raises(NombreDuplicadoError):
        servicio.ejecutar(materia_b.id, "redes")


def test_editar_materia_permite_guardar_sin_cambiar_el_nombre():
    repositorio = MateriaRepositoryFake()
    materia = repositorio.guardar(Materia(nombre="Redes"))
    servicio = EditarMateria(repositorio)

    servicio.ejecutar(materia.id, "Redes")

    assert repositorio.obtener(materia.id).nombre == "Redes"
