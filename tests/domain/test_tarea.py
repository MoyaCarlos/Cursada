from datetime import date, timedelta

import pytest

from domain.tarea import (
    EstadoTarea,
    PrioridadTarea,
    Tarea,
    cambiar_estado_tarea,
    crear_tarea,
    editar_tarea,
)


def test_crear_tarea_rechaza_titulo_vacio():
    with pytest.raises(ValueError):
        crear_tarea(materia_id=1, titulo="", fecha_limite=date(2026, 12, 31))


def test_crear_tarea_rechaza_titulo_solo_espacios():
    with pytest.raises(ValueError):
        crear_tarea(materia_id=1, titulo="   ", fecha_limite=date(2026, 12, 31))


def test_crear_tarea_rechaza_fecha_limite_pasada():
    ayer = date.today() - timedelta(days=1)
    with pytest.raises(ValueError):
        crear_tarea(materia_id=1, titulo="TP1", fecha_limite=ayer)


def test_crear_tarea_usa_prioridad_media_por_defecto():
    tarea = crear_tarea(materia_id=1, titulo="TP1", fecha_limite=date.today())

    assert tarea.prioridad == PrioridadTarea.MEDIA


def test_crear_tarea_nace_pendiente():
    tarea = crear_tarea(materia_id=1, titulo="TP1", fecha_limite=date.today())

    assert tarea.estado == EstadoTarea.PENDIENTE


def test_editar_tarea_actualiza_titulo():
    original = crear_tarea(materia_id=1, titulo="TP1", fecha_limite=date(2026, 12, 31))
    original.id = 10

    editada = editar_tarea(
        original, materia_id=1, titulo="TP1 final", fecha_limite=date(2026, 12, 31)
    )

    assert editada.titulo == "TP1 final"
    assert editada.id == 10


def test_editar_tarea_rechaza_titulo_vacio():
    original = crear_tarea(materia_id=1, titulo="TP1", fecha_limite=date(2026, 12, 31))

    with pytest.raises(ValueError):
        editar_tarea(original, materia_id=1, titulo="", fecha_limite=date(2026, 12, 31))


def test_editar_tarea_rechaza_fecha_nueva_pasada():
    original = crear_tarea(materia_id=1, titulo="TP1", fecha_limite=date.today())
    ayer = date.today() - timedelta(days=1)

    with pytest.raises(ValueError):
        editar_tarea(original, materia_id=1, titulo="TP1", fecha_limite=ayer)


def test_editar_tarea_permite_fecha_sin_cambios_aunque_este_vencida():
    vencida = date.today() - timedelta(days=5)
    original = Tarea(materia_id=1, titulo="TP1", fecha_limite=vencida, id=10)

    editada = editar_tarea(
        original,
        materia_id=1,
        titulo="TP1",
        fecha_limite=vencida,
        descripcion="nueva desc",
    )

    assert editada.descripcion == "nueva desc"
    assert editada.fecha_limite == vencida


def test_editar_tarea_preserva_estado():
    original = Tarea(
        materia_id=1,
        titulo="TP1",
        fecha_limite=date.today(),
        estado=EstadoTarea.EN_PROGRESO,
        id=5,
    )

    editada = editar_tarea(
        original, materia_id=1, titulo="TP1 v2", fecha_limite=date.today()
    )

    assert editada.estado == EstadoTarea.EN_PROGRESO


def test_cambiar_estado_tarea_actualiza_solo_el_estado():
    original = Tarea(
        materia_id=1,
        titulo="TP1",
        fecha_limite=date(2026, 12, 31),
        descripcion="algo",
        estado=EstadoTarea.PENDIENTE,
        id=7,
    )

    cambiada = cambiar_estado_tarea(original, EstadoTarea.EN_PROGRESO)

    assert cambiada.estado == EstadoTarea.EN_PROGRESO
    assert cambiada.titulo == "TP1"
    assert cambiada.descripcion == "algo"
    assert cambiada.id == 7


def test_cambiar_estado_tarea_permite_volver_a_pendiente():
    completada = Tarea(
        materia_id=1,
        titulo="TP1",
        fecha_limite=date(2026, 12, 31),
        estado=EstadoTarea.COMPLETADA,
        id=7,
    )

    cambiada = cambiar_estado_tarea(completada, EstadoTarea.PENDIENTE)

    assert cambiada.estado == EstadoTarea.PENDIENTE
