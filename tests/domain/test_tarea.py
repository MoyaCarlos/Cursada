from datetime import date, timedelta

import pytest

from domain.tarea import EstadoTarea, PrioridadTarea, crear_tarea


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
