from flask import request
from model_db.class_singlen import refresh, instancia_conexion
from datetime import date

def test_middleware_jwt_ausente_bloquea_acceso(client):
    response = client.get("/principal")

    assert response.status_code == 302

def test_middleware_jwt_ausente_bloquea_acceso(create_jwt_expirate):
    response = create_jwt_expirate.get("/principal", follow_redirects=True)

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Sesion expirate" in data_html

def test_middleware_jwt_refresh(create_jwt_expirate):
    get_uuid = create_jwt_expirate.get("/refreh")
    pool, cursor = instancia_conexion.iniciar_conexion()
    query, parameters = refresh.create_refresh(1, get_uuid.data, False, date.today())
    instancia_conexion.registrar(cursor, query, parameters)
    instancia_conexion.ejecutar_cambio(pool)

    response = create_jwt_expirate.get("/principal")
    assert response.status_code == 302


def test_middleware_jwt_correcto(create_jwt):
    response = create_jwt.get("/principal")

    assert response.status_code == 200

def test_middleware_nivel_acceso_no_permitido(create_jwt_worker):
    response = create_jwt_worker.get("/usuarios")

    assert response.status_code == 403

def test_middleware_nivel_acceso_permitido(create_jwt):
    response = create_jwt.get("/usuarios")

    assert response.status_code == 200
