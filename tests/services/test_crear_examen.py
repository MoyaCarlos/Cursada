from datetime import date, time

import pytest

from domain.examen import ModalidadExamen
from domain.materia import Materia, MateriaInexistenteError
from services.crear_examen import CrearExamen
from tests.fakes import ExamenRepositoryFake, MateriaRepositoryFake


def test_crear_examen_guarda_cuando_la_materia_existe():
    materias = MateriaRepositoryFake()
    materia = materias.guardar(Materia(nombre="Bases de Datos"))
    examenes = ExamenRepositoryFake()
    servicio = CrearExamen(examenes, materias)

    examen = servicio.ejecutar(
        materia_id=materia.id,
        tema="Parcial 1",
        fecha=date(2026, 11, 10),
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
    )

    assert examen.id is not None
    assert [e.tema for e in examenes.listar()] == ["Parcial 1"]


def test_crear_examen_rechaza_materia_inexistente():
    materias = MateriaRepositoryFake()
    examenes = ExamenRepositoryFake()
    servicio = CrearExamen(examenes, materias)

    with pytest.raises(MateriaInexistenteError):
        servicio.ejecutar(
            materia_id=999,
            tema="Parcial 1",
            fecha=date(2026, 11, 10),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
