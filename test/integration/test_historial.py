from model_db.class_singlen import instancia_conexion

def test_admin_y_trabajador_pueden_acceder_al_historial_lista_por_defecto_solo_movimientos_del_dia_actual(create_jwt, create_jwt_worker):
    response = create_jwt.get("/historia")

    response_worker = create_jwt_worker.get("/historia")

    data_html = response.data.decode("utf-8")
    data_html_worker = response_worker.data.decode("utf-8")

    assert response.status_code == 200
    assert response_worker.status_code == 200
    assert "No hay movimientos registrados" in data_html
    assert "No hay movimientos registrados" in data_html_worker

def test_historial_filtra_por_rango_de_siete_dias(create_jwt):
    response = create_jwt.get("/historia_filtro/5")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

def test_historial_filtra_por_mes_actual(create_jwt):
    response = create_jwt.get("/historia_filtro/6")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

def test_historial_filtra_por_movimientos_dia_actual(create_jwt):
    # Entrada
    response = create_jwt.get("/historia_filtro/1")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Salida
    response = create_jwt.get("/historia_filtro/2")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Devolucion
    response = create_jwt.get("/historia_filtro/3")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Ajuste
    response = create_jwt.get("/historia_filtro/4")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

def test_historial_filtra_por_intervalo_de_fechas_personalizado(create_jwt):
    response = create_jwt.get("/historial_intervalo?desde=2026-04-19&hasta=2026-04-30")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Motivo: Entrada de nuevo producto" in data_html

def test_historial_filtra_por_movimientos_intervalo_fechas(create_jwt):
    # Entrada
    response = create_jwt.get("/historial_intervalo_categoria?categoria=1&desde=2026-06-11&hasta=2026-06-26")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Salida
    response = create_jwt.get("/historial_intervalo_categoria?categoria=2&desde=2026-06-11&hasta=2026-06-26")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Devolucion
    response = create_jwt.get("/historial_intervalo_categoria?categoria=3&desde=2026-06-11&hasta=2026-06-26")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Ajuste
    response = create_jwt.get("/historial_intervalo_categoria?categoria=4&desde=2026-06-11&hasta=2026-06-26")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

def test_historial_busca_texto_en_el_historial_del_dia(create_jwt):
    response = create_jwt.get("/historia_search?buscar=pintura")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

def test_historial_busqueda_filtro_por_tipo_de_movimiento(create_jwt):
    response = create_jwt.get("/historia_search_filtro?buscar=pintura&categoria=5")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    response = create_jwt.get("/historia_search_filtro?buscar=pintura&categoria=6")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Entrada
    response = create_jwt.get("/historia_search_filtro?buscar=pintura&categoria=1")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Salida
    response = create_jwt.get("/historia_search_filtro?buscar=pintura&categoria=2")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Devolucion
    response = create_jwt.get("/historia_search_filtro?buscar=pintura&categoria=3")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Ajuste
    response = create_jwt.get("/historia_search_filtro?buscar=pintura&categoria=4")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

def test_historial_busqueda_por_intervalo_de_fechas_personalizado(create_jwt):
    response = create_jwt.get("/historia_search_intervalo?buscar=entrada&desde=2026-04-20&hasta=2026-04-30")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Motivo: Entrada de nuevo producto" in data_html

def test_historial_busqueda_filtro_por_tipo_de_movimiento_intervalo_de_fecha(create_jwt):
    # Entrada
    response = create_jwt.get("historia_search_intervalo_categoria?buscar=entrada&desde=2026-04-20&hasta=2026-06-30&categoria=1")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Motivo: Entrada de nuevo producto" in data_html

    # Salida
    response = create_jwt.get("historia_search_intervalo_categoria?buscar=entrada&desde=2026-04-20&hasta=2026-06-30&categoria=2")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Devolucion
    response = create_jwt.get("historia_search_intervalo_categoria?buscar=entrada&desde=2026-04-20&hasta=2026-06-30&categoria=3")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html

    # Ajuste
    response = create_jwt.get("historia_search_intervalo_categoria?buscar=entrada&desde=2026-04-20&hasta=2026-06-30&categoria=4")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "No hay movimientos registrados" in data_html