from model_db.class_singlen import instancia_conexion, productor

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
    
    