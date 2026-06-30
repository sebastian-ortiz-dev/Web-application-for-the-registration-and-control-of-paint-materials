from utils.obtener_fecha import este_mes, mes, dia
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

def teset_formato_fecha_hace_30_dias():
    today, days_ago = dia()

    assert type(today) == date
    assert type(today) != None
    assert type(days_ago) == date
    assert type(days_ago) != None

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