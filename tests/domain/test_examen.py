from datetime import date, time, timedelta

import pytest

from domain.examen import Examen, ModalidadExamen, crear_examen, editar_examen


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


def test_editar_examen_actualiza_tema():
    original = crear_examen(
        materia_id=1,
        tema="Parcial 1",
        fecha=date(2026, 11, 10),
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
    )
    original.id = 10

    editado = editar_examen(
        original,
        materia_id=1,
        tema="Parcial 1 - Reprogramado",
        fecha=date(2026, 11, 10),
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
    )

    assert editado.tema == "Parcial 1 - Reprogramado"
    assert editado.id == 10


def test_editar_examen_rechaza_tema_vacio():
    original = crear_examen(
        materia_id=1,
        tema="Parcial 1",
        fecha=date(2026, 11, 10),
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
    )

    with pytest.raises(ValueError):
        editar_examen(
            original,
            materia_id=1,
            tema="",
            fecha=date(2026, 11, 10),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )


def test_editar_examen_rechaza_fecha_nueva_pasada():
    original = crear_examen(
        materia_id=1,
        tema="Parcial 1",
        fecha=date.today(),
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
    )
    ayer = date.today() - timedelta(days=1)

    with pytest.raises(ValueError):
        editar_examen(
            original,
            materia_id=1,
            tema="Parcial 1",
            fecha=ayer,
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )


def test_editar_examen_permite_fecha_sin_cambios_aunque_este_vencida():
    vencida = date.today() - timedelta(days=5)
    original = Examen(
        materia_id=1,
        tema="Parcial 1",
        fecha=vencida,
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
        id=10,
    )

    editado = editar_examen(
        original,
        materia_id=1,
        tema="Parcial 1",
        fecha=vencida,
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
        notas="nueva nota",
    )

    assert editado.notas == "nueva nota"
    assert editado.fecha == vencida


def test_editar_examen_rechaza_hora_none():
    original = crear_examen(
        materia_id=1,
        tema="Parcial 1",
        fecha=date(2026, 11, 10),
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
    )

    with pytest.raises(ValueError):
        editar_examen(
            original,
            materia_id=1,
            tema="Parcial 1",
            fecha=date(2026, 11, 10),
            hora=None,
            modalidad=ModalidadExamen.PRESENCIAL,
        )


def test_editar_examen_rechaza_modalidad_none():
    original = crear_examen(
        materia_id=1,
        tema="Parcial 1",
        fecha=date(2026, 11, 10),
        hora=time(14, 0),
        modalidad=ModalidadExamen.PRESENCIAL,
    )

    with pytest.raises(ValueError):
        editar_examen(
            original,
            materia_id=1,
            tema="Parcial 1",
            fecha=date(2026, 11, 10),
            hora=time(14, 0),
            modalidad=None,
        )
