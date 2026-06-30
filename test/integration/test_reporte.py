def test_generar_reporte_diario(create_jwt):
    response = create_jwt.get("/reporte", follow_redirects=True)

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Reporte Creado" in data_html

def test_generar_reporte_mensual(create_jwt):
    response = create_jwt.get("/reporte_mensual", follow_redirects=True)

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Reporte Creado" in data_html
