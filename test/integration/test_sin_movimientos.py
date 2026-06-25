from model_db.class_singlen import instancia_conexion, productor

def test_admin_y_trabajador_pueden_acceder_al_listado_solo_productos_sin_movimiento(create_jwt, create_jwt_worker):
    pool, cursor = instancia_conexion.iniciar_conexion()
    instancia_conexion.registrar(cursor, "INSERT INTO producto (nombre_producto, descripcion, precio_venta, cantidad, fecha_actualizacion, imagen, id_distribuidor, borrado, id_categoria, id_medida, last_moviment, cantidad_minima) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("pintura marron", "marron", 10.00, 50, "2026-01-18", "pintura.jpg", 1, "False", 1, 1, "True",5))
    instancia_conexion.ejecutar_cambio(pool)
    instancia_conexion.registrar(cursor, "INSERT INTO producto (nombre_producto, descripcion, precio_venta, cantidad, fecha_actualizacion, imagen, id_distribuidor, borrado, id_categoria, id_medida, last_moviment, cantidad_minima) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("pintura beige", "beige", 10.00, 50, "2026-01-18", "pintura.jpg", 1, "False", 1, 1, "True",5))
    instancia_conexion.ejecutar_cambio(pool)
    instancia_conexion.cerrar_conexion(cursor, pool)

    response = create_jwt.get("/sin_movimientos")
    response_worker = create_jwt_worker.get("/sin_movimientos")

    data_html = response.data.decode("utf-8")
    data_html_worker = response_worker.data.decode("utf-8")

    assert response.status_code == 200
    assert response_worker.status_code == 200
    assert "/detalles/6" in data_html
    assert "/detalles/6" in data_html_worker

def test_filtrar_por_categoria_sin_movimiento(create_jwt):
    response = create_jwt.get("/tipo_listado/1")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/7" in data_html

def test_busqueda_por_proveedor_en_lista_sin_movimiento(create_jwt):
    response = create_jwt.get("/por_proveedores_no_movimientos")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/6" in data_html
    assert "/detalles/7" in data_html

def test_busqueda_por_nombre_en_lista_sin_movimiento(create_jwt):
    response = create_jwt.get("/search_bar_no_movimientos?buscar=pintura+beige")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/7" in data_html

def test_busqueda_por_proveedor_en_lista_sin_movimiento(create_jwt):
    response = create_jwt.get("/por_proveedores_search_sin_movimiento?buscar=pintura")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Proveedor: proveedor primero" in data_html
    assert "/detalles/7" in data_html

def test_busqueda_combinada_nombre_y_categoria(create_jwt):
    response = create_jwt.get("/filtro_no_movientos_search?buscar=pintura+marron&categoria=1")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/6" in data_html