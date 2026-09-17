import pytest

from domain.materia import crear_materia


def test_crear_materia_rechaza_nombre_vacio():
    with pytest.raises(ValueError):
        crear_materia("")


def test_crear_materia_rechaza_nombre_solo_espacios():
    with pytest.raises(ValueError):
        crear_materia("   ")


def test_crear_materia_recorta_espacios_al_inicio_y_final():
    materia = crear_materia("  Bases de Datos  ")

    assert materia.nombre == "Bases de Datos"
