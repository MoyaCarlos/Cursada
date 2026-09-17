import pytest

from domain.materia import EventosAsociadosError, Materia
from services.eliminar_materia import EliminarMateria
from tests.fakes import MateriaRepositoryFake


def test_eliminar_materia_sin_eventos_asociados():
    repositorio = MateriaRepositoryFake()
    materia = repositorio.guardar(Materia(nombre="Redes"))
    servicio = EliminarMateria(repositorio)

    servicio.ejecutar(materia.id)

    assert repositorio.obtener(materia.id) is None


def test_eliminar_materia_bloquea_si_tiene_eventos_asociados():
    repositorio = MateriaRepositoryFake()
    materia = repositorio.guardar(Materia(nombre="Redes"))
    repositorio.marcar_con_eventos(materia.id)
    servicio = EliminarMateria(repositorio)

    with pytest.raises(EventosAsociadosError):
        servicio.ejecutar(materia.id)

    assert repositorio.obtener(materia.id) is not None
