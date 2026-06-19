from model_db.class_singlen import instancia_conexion, proveedor

def test_listar_proveedor(create_jwt):
    pool, cursor = instancia_conexion.iniciar_conexion()
    query, variables = proveedor.create_proveedor("Manpica", "manpica@gmail.com", "Los Teques", "0414658963", "58-561389632", "2026-06-19")
    instancia_conexion.registrar(cursor, query, variables)
    query, variables = proveedor.create_proveedor("Pintu", "Pintu@gmail.com", "Caracas barquisimetro", "0414658985", "58-564789632", "2026-06-19")
    instancia_conexion.registrar(cursor, query, variables)
    instancia_conexion.ejecutar_cambio(pool)
    instancia_conexion.cerrar_conexion(cursor, pool)
    response = create_jwt.get("/proveedores")

    data_html = response.data.decode("utf-8")

    assert "/edit_proveedor/1" in data_html

def test_buscar_proveedor(create_jwt):
    response = create_jwt.get("/buscar_proveedor?buscar=pintu")

    data_html = response.data.decode("utf-8")

    assert "/edit_proveedor/3" in data_html

def test_admin_puede_crear(create_jwt):
    data_create = {"nombre": "williafro", "correo": "willi@gmail.com", "direccion": "guarenas", "telefono": "04123567777", "rif": "58-978641354777",}
    
    response = create_jwt.post("/crear_proveedor", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    proveedor_create = instancia_conexion.uno(cursor, "SELECT id_distribuidor FROM distribuidor WHERE nombre = %s AND borrado = FALSE", (data_create["nombre"],)) 
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert proveedor_create == (4,)

def test_admin_puede_modificar(create_jwt):
    data_update = {"nombre": "proveedor primero", "correo": "proveedor@gmail.com", "direccion": "San antonio de los altos", "telefono": "0414-325-56-77", "rif": "j-555656535",}
    
    response = create_jwt.post("/cambios_proveedor/1", data=data_update)

    pool, cursor = instancia_conexion.iniciar_conexion()
    proveedor_create = instancia_conexion.uno(cursor, "SELECT id_distribuidor FROM distribuidor WHERE nombre = %s AND borrado = FALSE", (data_update["nombre"],)) 
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert proveedor_create == (1,)

def test_admin_elimina_proveedor(create_jwt):
    response = create_jwt.post("/delete_proveedor/4")

    pool, cursor = instancia_conexion.iniciar_conexion()
    proveedor_create = instancia_conexion.uno(cursor, "SELECT id_distribuidor FROM distribuidor WHERE id_distribuidor = %s AND borrado = TRUE", (4,)) 
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert proveedor_create == (4,)

def test_trabajador_no_puede_crear_proveedor(create_jwt_worker):
    data_create = {"nombre": "proveedor maestro", "correo": "maestro@gmail.com", "direccion": "guarenas", "telefono": "04123567895", "rif": "58-97864135466",}
    
    response = create_jwt_worker.post("/crear_proveedor", data=data_create)

    pool, cursor = instancia_conexion.iniciar_conexion()
    proveedor_create = instancia_conexion.uno(cursor, "SELECT id_distribuidor FROM distribuidor WHERE nombre = %s AND borrado = FALSE", (data_create["nombre"],)) 
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 403
    assert proveedor_create == None

def test_trabajador_no_puede_editar_proveedor(create_jwt_worker):
    data_update = {"nombre": "pintu nuevo", "correo": "maestro@gmail.com", "direccion": "guarenas", "telefono": "04123567895", "rif": "58-97864135466",}
    
    response = create_jwt_worker.post("/cambios_proveedor/3", data=data_update)

    pool, cursor = instancia_conexion.iniciar_conexion()
    proveedor_create = instancia_conexion.uno(cursor, "SELECT id_distribuidor FROM distribuidor WHERE nombre = %s AND borrado = FALSE", (data_update["nombre"],)) 
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 403
    assert proveedor_create == None

def test_trabajador_no_puede_eliminar_proveedor(create_jwt_worker):
    response = create_jwt_worker.post("/delete_proveedor/2")

    pool, cursor = instancia_conexion.iniciar_conexion()
    proveedor_create = instancia_conexion.uno(cursor, "SELECT id_distribuidor FROM distribuidor WHERE id_distribuidor = %s AND borrado = TRUE", (2,)) 
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 403
    assert proveedor_create == None