from services.generar_reporte import generar_reporte_diario
def test_403_ruta_no_accede_nivel_acceso_retorna_plantilla_correcta(create_jwt_worker):
    response = create_jwt_worker.get('/usuarios')

    data_html = response.data.decode("utf-8")
    
    assert response.status_code == 403
    assert "Forbidden" in data_html

def test_404_ruta_inexistente_retorna_plantilla_correcta(create_jwt):
    response = create_jwt.get('/ruta_que_no_existe_12345')

    data_html = response.data.decode("utf-8")
    
    assert response.status_code == 404
    assert "Resource not found" in data_html

def test_405_metodo_no_permitido(create_jwt):
    response = create_jwt.get('/crear_usuario') 
    
    data_html = response.data.decode("utf-8")

    assert response.status_code == 405
    assert 'Method not allowed' in data_html

def test_500_error_interno(create_jwt):
    response = create_jwt.get("/error-forzado")
    
    data_html = response.data.decode("utf-8")

    assert response.status_code == 500
    assert 'Internal Server Error' in data_html