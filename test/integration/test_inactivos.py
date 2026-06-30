from model_db.class_singlen import instancia_conexion, productor, proveedor, usuarios

def test_trabajador_recibe_403_en_todas_las_vistas_de_inactivos(create_jwt_worker):
    reponse = create_jwt_worker.get("/inactivos")

    assert reponse.status_code == 403

def test_admin_ve_productos_desactivados_en_lista(create_jwt):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    productos, parametro = productor.create_producto("guantes", "guantes", 10, 10, "2026-06-18", "pintura.jpg", 1, 2, 1, 5)
    instancia_conexion.registrar(cursor, productos, parametro)
    instancia_conexion.ejecutar_cambio(pool_db)

    query, variable = productor.eliminar_producto(2)
    instancia_conexion.registrar(cursor, query, variable)
    instancia_conexion.ejecutar_cambio(pool_db)

    instancia_conexion.cerrar_conexion(cursor, pool_db)
    response = create_jwt.get("/inactivos")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/2" in data_html

def test_admin_busca_producto_inactivo_por_nombre(create_jwt):
    response = create_jwt.get("/busqueda_producto_inactivo?buscar=guantes")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/2" in data_html

def test_admin_reintegra_producto_inactivo_exitosamente(create_jwt):
    response = create_jwt.post("/recuperar_producto/2")

    pool_db, cursor = instancia_conexion.iniciar_conexion()
    obtenido = instancia_conexion.uno(cursor, "SELECT borrado FROM producto WHERE id_producto = %s", (2,))
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    assert response.status_code == 302
    assert obtenido[0] == False

def test_admin_ve_proveedores_desactivados_en_lista(create_jwt):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    prove, variables = proveedor.create_proveedor("cashea", "cashea@gmail.com", "Los teques", "041568935", "7-56231261323", "2026-06-24")
    instancia_conexion.registrar(cursor, prove, variables)
    
    delete, variables = proveedor.eliminar_proveedor(2)
    instancia_conexion.registrar(cursor, delete, variables)
    instancia_conexion.ejecutar_cambio(pool_db)

    instancia_conexion.cerrar_conexion(cursor, pool_db)
    response = create_jwt.get("/inactivos_proveedor")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/edit_proveedor/2" in data_html

def test_admin_busca_proveedor_inactivo_por_nombre(create_jwt):
    response = create_jwt.get("/buscar_proveedor_inactivo?buscar=cashea")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/edit_proveedor/2" in data_html

def test_admin_reintegra_proveedor_inactivo_exitosamente(create_jwt):
    response = create_jwt.post("/recuperar_proveedor/2")

    pool_db, cursor = instancia_conexion.iniciar_conexion()
    obtenido = instancia_conexion.uno(cursor, "SELECT borrado FROM distribuidor WHERE id_distribuidor = %s", (2,))
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    assert response.status_code == 302
    assert obtenido[0] == False

def test_admin_ve_usuarios_desactivados_en_lista(create_jwt):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    usuario, variables = usuarios.create_usuario("carlos", "$argon2id$v=19$m=65536,t=3,p=4$f2kkd1t6h1nYMRI6XNT6KQ$1ogddX5jZbDWA1W3PiOfphLIltaywzNDxYo5yyx/3Oc", 2, "usuario_defecto.png", "2026-06-24")
    instancia_conexion.registrar(cursor, usuario, variables)
    
    delete, variables = usuarios.eliminar_usuario(3)
    instancia_conexion.registrar(cursor, delete, variables)
    instancia_conexion.ejecutar_cambio(pool_db)

    instancia_conexion.cerrar_conexion(cursor, pool_db)

    response = create_jwt.get("/inactivos_perfiles")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/usuario_detalles/3" in data_html

def test_admin_busca_usuario_inactivo_por_nombre(create_jwt):
    response = create_jwt.get("/busqueda_perfiles_inactivo?buscar=carlos")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/usuario_detalles/3" in data_html

def test_admin_reintegra_usuario_inactivo_exitosamente(create_jwt):
    response = create_jwt.post("/recuperar_perfil/3")

    pool_db, cursor = instancia_conexion.iniciar_conexion()
    obtenido = instancia_conexion.uno(cursor, "SELECT borrado FROM usuario WHERE id_usuario = %s", (3,))
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    assert response.status_code == 302
    assert obtenido[0] == False