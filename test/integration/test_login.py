def test_login_exitoso(client):
    credentials = ["admin", "123"]

    response = client.post("/login", data={"usuario": credentials[0], "clave": credentials[1],}, follow_redirects=True)

    data_html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "DashBoard" in data_html
    assert response.request.path == "/principal"

def test_login_fallido_contrasena_incorrecta(client):
    credentials = ["admin", "156"]

    response = client.post("/login", data={"usuario": credentials[0], "clave": credentials[1],}, follow_redirects=True)

    data_html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Login" in data_html
    assert response.request.path == "/login"
