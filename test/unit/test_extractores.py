from utils.sin_movimientos import sin_movimiento, limpiar

def test_sin_movimientos_con_lista_vacia_devuelve_set():
    id_productos = [5,4,6,2,3,8]
    id_movimientos = [2,3,8]

    response = sin_movimiento(id_productos, id_movimientos)

    assert response == {4, 5, 6}
    assert type(response) == set
    assert response != None

def test_sin_movimientos_con_datos_devuelve_lista_vacia():
    id_productos = None
    id_movimientos = None

    response = sin_movimiento(id_productos, id_movimientos)

    assert response == []
    assert type(response) == list
    assert response != None

def test_limpiar_id_con_datos_brutos_extrae_arreglo_de_ids():
    datos_postgres_tuples = [(101, "Tubo PVC 1/2"), (102, "Llave de paso"), (103, "Cinta teflón")]

    response = limpiar(datos_postgres_tuples)

    assert response == [101, 102, 103]
    assert response != None

def test_obtener_proveedores_con_lista_vacia_devuelve_lista_vacia():
    datos_postgres_tuples_empty = []

    response = limpiar(datos_postgres_tuples_empty)

    assert response == []
    assert response != None

def test_obtener_proveedores_con_datos_brutos_extrae_campos_correctos():
    datos_postgres_tuples = [(101, "Tubo PVC 1/2"), (102, "Llave de paso"), (103, "Cinta teflón")]

    response = limpiar(datos_postgres_tuples)

    assert response == [101, 102, 103]
    assert response != None

def test_obtener_proveedores_con_lista_vacia_devuelve_lista_vacia():
    datos_postgres_tuples_empty = []

    response = limpiar(datos_postgres_tuples_empty)

    assert response == []
    assert response != None