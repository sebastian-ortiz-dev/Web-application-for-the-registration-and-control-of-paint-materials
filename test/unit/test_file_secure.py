from secure.file_secure import allowed_file

def test_extension_permitida():
    filename = "user.png"

    response = allowed_file(filename)

    assert response == True

def test_extension_no_permitida():
    filename = "user.txt"

    response = allowed_file(filename)

    assert response == False

def test_nombre_con_caracteres_raros_o_rutas_devuelve_false():
    filename = "  Mi Foto De Perfil #2026!!! .png  "

    response = allowed_file(filename)
    
    assert response == False