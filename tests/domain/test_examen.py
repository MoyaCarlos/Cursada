from datetime import date, time, timedelta

import pytest

from domain.examen import ModalidadExamen, crear_examen


def test_crear_examen_rechaza_tema_vacio():
    with pytest.raises(ValueError):
        crear_examen(
            materia_id=1,
            tema="",
            fecha=date(2026, 11, 10),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )


def test_crear_examen_rechaza_fecha_pasada():
    ayer = date.today() - timedelta(days=1)
    with pytest.raises(ValueError):
        crear_examen(
            materia_id=1,
            tema="Parcial 1",
            fecha=ayer,
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )


def test_crear_examen_rechaza_sin_hora():
    with pytest.raises(ValueError):
        crear_examen(
            materia_id=1,
            tema="Parcial 1",
            fecha=date.today(),
            hora=None,
            modalidad=ModalidadExamen.PRESENCIAL,
        )


def test_crear_examen_rechaza_sin_modalidad():
    with pytest.raises(ValueError):
        crear_examen(
            materia_id=1,
            tema="Parcial 1",
            fecha=date.today(),
            hora=time(14, 0),
            modalidad=None,
        )


def test_crear_examen_con_datos_validos():
    examen = crear_examen(
        materia_id=1,
        tema="Parcial 1",
        fecha=date.today(),
        hora=time(14, 0),
        modalidad=ModalidadExamen.VIRTUAL,
    )

    assert examen.tema == "Parcial 1"
    assert examen.modalidad == ModalidadExamen.VIRTUAL
    assert examen.notas == ""
