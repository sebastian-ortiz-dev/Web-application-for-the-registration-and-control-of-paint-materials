from model_db.class_singlen import instancia_conexion, productor
import io

def test_render_inventario_completo(create_jwt):
    pool, cursor = instancia_conexion.iniciar_conexion()
    query, variables = productor.create_producto("pintura blanca", "blanco", 10.00, 50, "2026-06-18", "pintura.jpg", 1, 1, 1, 5)
    instancia_conexion.registrar(cursor, query, variables)
    query, variables = productor.create_producto("pintura verde", "verde", 10.00, 50, "2026-06-18", "pintura.jpg", 1, 1, 1, 5)
    instancia_conexion.registrar(cursor, query, variables)
    instancia_conexion.ejecutar_cambio(pool)
    instancia_conexion.cerrar_conexion(cursor, pool)

    response = create_jwt.get("/")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/1" in data_html
    assert "/detalles/2" in data_html

def test_render_inventario_completo_trabajador(create_jwt_worker):
    response = create_jwt_worker.get("/trabajador")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/1" in data_html
    assert "/detalles/2" in data_html
    
def test_busqueda_inventario(create_jwt):
    response = create_jwt.get("search_bar?buscar=pintura+roja")   

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/1" in data_html

def test_filtrar_inventario_por_categoria(create_jwt):
    response = create_jwt.get("/tipo/1")   

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/1" in data_html
    assert "/detalles/2" in data_html
    assert "/detalles/3" in data_html

def test_filtrar_inventario_por_categoria_busqueda(create_jwt):
    response = create_jwt.get("filtro_search?buscar=pintura+blanca&categoria=1")   

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/detalles/2" in data_html

def test_filtrar_inventario_por_proveedor(create_jwt):
    response = create_jwt.get("/por_proveedores")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "proveedor" in data_html
    assert "/detalles/1" in data_html
    assert "/detalles/2" in data_html

def test_filtrar_inventario_por_proveedor_busqueda(create_jwt):
    response = create_jwt.get("/por_proveedores_search?buscar=pintura+verde")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "proveedor" in data_html
    assert "/detalles/3" in data_html

def test_admin_puede_modificar_producto(create_jwt):
    imagen_vacia = (io.BytesIO(b""), "")
    data_update = {"imagen": imagen_vacia, "nombre": "pintura roja", "detalles": "pintura roja clara", "precio": 30.00, "existencia": 50, "distribuidor": 1, "medida": 1, "categoria": 1, "minima": 5,}
    
    response = create_jwt.post("/cambios_producto/1", data=data_update)

    assert response.status_code == 302

def test_admin_puede_borrar_producto(create_jwt):
     
    response = create_jwt.post("/delete_producto/1")

    assert response.status_code == 302

def test_trabajador_no_puede_editar_producto(create_jwt_worker):
    imagen_vacia = (io.BytesIO(b""), "")
    data_update = {"imagen": imagen_vacia, "nombre": "pintura roja", "detalles": "pintura roja clara", "precio": 30.00, "existencia": 50, "distribuidor": 1, "medida": 1, "categoria": 1, "minima": 5,}
    
    response = create_jwt_worker.post("/cambios_producto/1", data=data_update)

    assert response.status_code == 403

def test_trabajador_no_puede_borrar_producto(create_jwt_worker):
    response = create_jwt_worker.post("/delete_producto/1")

    assert response.status_code == 403