from datetime import date

import pytest

from ui.formato_fecha import formatear_fecha, parsear_fecha


def test_parsear_fecha_completa():
    assert parsear_fecha("15/10/2026") == date(2026, 10, 15)


def test_parsear_fecha_sin_anio_usa_el_anio_actual():
    hoy = date.today()
    assert parsear_fecha("15/10") == date(hoy.year, 10, 15)


def test_parsear_fecha_invalida_lanza_value_error():
    with pytest.raises(ValueError):
        parsear_fecha("no es una fecha")


def test_formatear_fecha():
    assert formatear_fecha(date(2026, 10, 15)) == "15/10/2026"
