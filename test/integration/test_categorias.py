from model_db.class_singlen import instancia_conexion

def test_mostrar_medidas_categorias(create_jwt):
    reponse = create_jwt.get("/configuracion")

    data_html = reponse.data.decode("utf-8")

    assert "Medidas:" in data_html

def test_trabajador_no_puede_crear_categoria(create_jwt_worker):
    data_create = {"nombre": "Herramientas de aplicacion"}

    reponse = create_jwt_worker.post("/crear_categoria", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    categoria = instancia_conexion.uno(cursor, "SELECT * FROM categorias c WHERE c.categoria = %s", (data_create["nombre"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert reponse.status_code == 403
    assert categoria == None

def test_trabajador_no_puede_editar_categoria(create_jwt_worker):
    data_create = {"nombre": "Herramientas de aplicacion prueba"}

    reponse = create_jwt_worker.post("/modificar_categoria/1", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    categoria = instancia_conexion.uno(cursor, "SELECT * FROM categorias c WHERE c.categoria = %s", (data_create["nombre"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert reponse.status_code == 403
    assert categoria == None

def test_admin_puede_crear_categoria(create_jwt):
    data_create = {"nombre": "Herramientas de hogar"}

    reponse = create_jwt.post("/crear_categoria", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    categoria = instancia_conexion.uno(cursor, "SELECT * FROM categorias c WHERE c.categoria = %s", (data_create["nombre"],))
    instancia_conexion.cerrar_conexion(cursor, pool)
    categoria = (categoria[0], categoria[1].strip())

    assert reponse.status_code == 302
    assert categoria == (2, "Herramientas de hogar")

def test_admin_puede_modificar_categoria(create_jwt):
    data_create = {"nombre": 'Herramientas de proteccion'}

    reponse = create_jwt.post("/modificar_categoria/2", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    categoria = instancia_conexion.uno(cursor, "SELECT * FROM categorias c WHERE c.categoria = %s", (data_create["nombre"],))
    instancia_conexion.cerrar_conexion(cursor, pool)
    categoria = (categoria[0], categoria[1].strip())

    assert reponse.status_code == 302
    assert categoria == (2, 'Herramientas de proteccion')

