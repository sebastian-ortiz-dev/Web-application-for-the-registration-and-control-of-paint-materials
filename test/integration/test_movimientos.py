from model_db.class_singlen import instancia_conexion, productor
from PIL import Image
import io

def test_entrada_producto_existente_incrementa_stock_y_redirige(create_jwt):
    data_insert = {"producto": 1, "cantidad_entrada": 20}

    response = create_jwt.post("/registrar_entrada_existente", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (1, 70)

# terminalo 
def test_entrada_producto_nuevo_crea_registro_y_redirige(create_jwt):
    imagen = Image.new("RGB", [100,100], color='red')

    image_bytes = io.BytesIO()
    imagen.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    nuevo_producto_data = {'nombre': "Tubo PVC 1/2", 'detalles': "Tubo de alta presión para agua limpia", 'imagen': (image_bytes, "tubo.png"), 'precio': 10, 'existencia': 100, 'distribuidor': 1, 'medida': 1, 'categoria': 1, 'minimo': 5,}

    response = create_jwt.post("/registrar_entrada_no_existente", data=nuevo_producto_data)

    query, parameters = productor.obtene_por_nombre(nuevo_producto_data["nombre"], nuevo_producto_data["detalles"], nuevo_producto_data["precio"], nuevo_producto_data["existencia"], nuevo_producto_data["minimo"])

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, query, parameters)
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (5,)

def test_registrar_salida_exito_disminuye_stock(create_jwt):
    data_insert = {"producto": 1, "cantidad_salida": 10}

    response = create_jwt.post("/registrar_salida", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (1, 60)

def test_salida_mayor_a_existencia(create_jwt):
    data_insert = {"producto": 2, "cantidad_salida": 100}

    response = create_jwt.post("/registrar_salida", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (2, 2)

def test_registrar_ajuste_negativo_stock(create_jwt):
    data_insert = {"producto": 3, "cantidad_ajuste": 1, "tipo": "1"}

    response = create_jwt.post("/registrar_Ajuste", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (3, 1)

def test_registrar_ajuste_negativo_stock_mayor_existencia(create_jwt):
    data_insert = {"producto": 3, "cantidad_ajuste": 40, "tipo": "1"}

    response = create_jwt.post("/registrar_Ajuste", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (3, 1)

def test_registrar_ajuste_positivo_stock(create_jwt):
    data_insert = {"producto": 3, "cantidad_ajuste": 24, "tipo": "2"}

    response = create_jwt.post("/registrar_Ajuste", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (3, 25)

def test_registrar_devolucion_cliente(create_jwt):
    data_insert = {"producto": 3, "motivo": "test devolucion de cliente", "cantidad_devolucion": 5, "tipo": "2"}

    response = create_jwt.post("/registrar_devolucion", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (3, 30)

def test_registrar_devolucion_proveedor(create_jwt):
    data_insert = {"producto": 3, "motivo": "test devolucion a proveedor", "cantidad_devolucion": 5, "tipo": "1"}

    response = create_jwt.post("/registrar_devolucion", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (3, 25)

def test_registrar_devolucion_proveedor_excede_cantidad(create_jwt):
    data_insert = {"producto": 3, "motivo": "test devolucion a proveedor excede", "cantidad_devolucion": 50, "tipo": "1"}

    response = create_jwt.post("/registrar_devolucion", data=data_insert)

    pool,cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.uno(cursor, "SELECT producto.id_producto, producto.cantidad FROM producto WHERE id_producto = %s", (data_insert["producto"],))
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert producto == (3, 25)