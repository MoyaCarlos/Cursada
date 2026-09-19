from datetime import date, time

import pytest

from domain.examen import Examen, ModalidadExamen
from domain.materia import Materia, MateriaInexistenteError
from services.editar_examen import EditarExamen
from tests.fakes import ExamenRepositoryFake, MateriaRepositoryFake


def test_editar_examen_guarda_cuando_la_materia_existe():
    materias = MateriaRepositoryFake()
    materia = materias.guardar(Materia(nombre="Bases de Datos"))
    examenes = ExamenRepositoryFake()
    examen = examenes.guardar(
        Examen(
            materia_id=materia.id,
            tema="Parcial 1",
            fecha=date(2026, 11, 10),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
    )
    servicio = EditarExamen(examenes, materias)

    servicio.ejecutar(
        id=examen.id,
        materia_id=materia.id,
        tema="Parcial 1 final",
        fecha=date(2026, 11, 10),
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
    )

    assert examenes.obtener(examen.id).tema == "Parcial 1 final"


def test_editar_examen_rechaza_materia_inexistente():
    materias = MateriaRepositoryFake()
    materia = materias.guardar(Materia(nombre="Bases de Datos"))
    examenes = ExamenRepositoryFake()
    examen = examenes.guardar(
        Examen(
            materia_id=materia.id,
            tema="Parcial 1",
            fecha=date(2026, 11, 10),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
    )
    servicio = EditarExamen(examenes, materias)

    with pytest.raises(MateriaInexistenteError):
        servicio.ejecutar(
            id=examen.id,
            materia_id=999,
            tema="Parcial 1",
            fecha=date(2026, 11, 10),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
