from secure.hash_password import Hash_password

hash = Hash_password()

def test_hasheo_contrasena_exitoso():
    password = "MiClaveSegura123"

    response = hash.create_hash(password)

    assert type(response) == str
    assert response != password
    assert response.startswith("$argon2") == True

def test_verificar_contrasena_correcta_devuelve_true():
    password = "MiClaveSegura123"
    hash_db = "$argon2id$v=19$m=65536,t=3,p=4$CJlt6ccXZEW8PGCyek4GIQ$zoPmc/tEufXA2vjRkT9HNhqnV9kWql4vStXRlvc5Fwc"

    response = hash.hash_password_verify(hash_db, password, "no","no", "no", "no", "no")

    assert response == True

def test_verificar_contrasena_incorrecta_devuelve_false():
    password_incorrect = "MiClaveIncorrecta123"
    hash_db = "$argon2id$v=19$m=65536,t=3,p=4$CJlt6ccXZEW8PGCyek4GIQ$zoPmc/tEufXA2vjRkT9HNhqnV9kWql4vStXRlvc5Fwc"

    response = hash.hash_password_verify(hash_db, password_incorrect, "no","no", "no", "no", "no")

    assert response == False