from secure.obtener_fecha import este_mes, mes
from datetime import date

def test_formato_fecha_salida_es_correcto_este_mes():
    date_over_ten = date(2026, 6, 12)
    date_down_ten = date(2026, 5, 9)

    response = este_mes(date_over_ten)

    assert type(response) != date
    assert type(response) == str

    response = este_mes(date_down_ten)

    assert type(response) != date
    assert type(response) == str

def test_formato_fecha_salida_es_correcto_mes():
    date_over_ten = date(2026, 6, 12)
    date_down_ten = date(2026, 5, 9)

    response = mes(date_over_ten)

    assert type(response) != date
    assert type(response) == str

    response = mes(date_down_ten)

    assert type(response) != date
    assert type(response) == str

def test_manejo_fecha_borde_o_vacia_este_mes():
    date_void = None

    response = este_mes(date_void)

    assert type(response) != date
    assert type(response) == str

def test_manejo_fecha_borde_o_vacia_mes():
    date_void = None

    response = mes(date_void)

    assert type(response) != date
    assert type(response) == str