from model_db.class_singlen import instancia_conexion

def test_trabajador_no_puede_crear_medida(create_jwt_worker):
    data_create = {"nombre": "pote"}

    reponse = create_jwt_worker.post("/crear_medida", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    categoria = instancia_conexion.uno(cursor, "SELECT * FROM unidad_medida u WHERE u.medida = %s", (data_create["nombre"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert reponse.status_code == 403
    assert categoria == None

def test_trabajador_no_puede_editar_medida(create_jwt_worker):
    data_create = {"nombre": "tobo prueba"}

    reponse = create_jwt_worker.post("/modificar_medida/1", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    categoria = instancia_conexion.uno(cursor, "SELECT * FROM unidad_medida u WHERE u.medida = %s", (data_create["nombre"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert reponse.status_code == 403
    assert categoria == None

def test_admin_puede_crear_medida(create_jwt):
    data_create = {"nombre": "Litro"}

    reponse = create_jwt.post("/crear_medida", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    categoria = instancia_conexion.uno(cursor, "SELECT * FROM unidad_medida u WHERE u.medida = %s", (data_create["nombre"],))
    instancia_conexion.cerrar_conexion(cursor, pool)
    categoria = (categoria[0], categoria[1].strip())

    assert reponse.status_code == 302
    assert categoria == (2, "Litro")

def test_admin_puede_modificar_medida(create_jwt):
    data_create = {"nombre": 'Unidad'}

    reponse = create_jwt.post("/modificar_medida/2", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    categoria = instancia_conexion.uno(cursor, "SELECT * FROM unidad_medida u WHERE u.medida = %s", (data_create["nombre"],))
    instancia_conexion.cerrar_conexion(cursor, pool)
    categoria = (categoria[0], categoria[1].strip())

    assert reponse.status_code == 302
    assert categoria == (2, 'Unidad')