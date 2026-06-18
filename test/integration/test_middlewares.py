def test_middleware_jwt_ausente_bloquea_acceso(client):
    response = client.get("/principal")

    assert response.status_code == 302

