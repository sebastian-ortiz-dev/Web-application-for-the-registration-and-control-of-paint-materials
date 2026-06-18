from model_db.class_singlen import instancia_conexion, productor

def test_render_productos_minimos_vacio(create_jwt):
    response = create_jwt.get("/alerta")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay productos con stock bajo" in data_html

def test_render_solo_productos_bajo_minimo(create_jwt):
    pool, cursor = instancia_conexion.iniciar_conexion()
    query, variables = productor.modifica_cantidad(2, 2)
    instancia_conexion.registrar(cursor, query, variables)
    query, variables = productor.modifica_cantidad(3, 2)
    instancia_conexion.registrar(cursor, query, variables)
    instancia_conexion.ejecutar_cambio(pool)
    instancia_conexion.cerrar_conexion(cursor, pool)


    response = create_jwt.get("/alerta")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/2" in data_html
    assert "/detalles/3" in data_html

def test_busqueda_en_productos_minimos(create_jwt):
    response = create_jwt.get("/search_bar_minimo?buscar=pintura")
    
    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/2" in data_html
    assert "/detalles/3" in data_html

def test_filtrar_productos_minimos_por_proveedor(create_jwt):
    response = create_jwt.get("/por_proveedores_minimo")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "proveedor" in data_html
    assert "/detalles/2" in data_html
    assert "/detalles/3" in data_html

def test_busqueda_productos_minimos_por_proveedo(create_jwt):
    response = create_jwt.get("/por_proveedores_search_minimo?buscar=pintura+blanca")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "proveedor" in data_html
    assert "/detalles/2" in data_html
    assert "/detalles/3" not in data_html

def test_filtrar_productos_minimos_por_categoria(create_jwt):
    response = create_jwt.get("/tipo_minimo/1")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/2" in data_html
    assert "/detalles/3" in data_html

def test_busqueda_productos_minimos_por_categoria(create_jwt):
    response = create_jwt.get("/por_proveedores_search_minimo?buscar=pintura+verde")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/2" not in data_html
    assert "/detalles/3" in data_html