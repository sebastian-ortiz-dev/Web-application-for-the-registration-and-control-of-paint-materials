from model_db.class_singlen import instancia_conexion, usuarios
import io
from PIL import Image

def test_trabajador_recibe_403_al_gestionar_usuarios(create_jwt_worker):
    response = create_jwt_worker.get("/usuarios")

    assert response.status_code == 403

def test_admin_listar_usuarios(create_jwt):
    response = create_jwt.get("/usuarios")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/usuario_detalles/2" in data_html 

def test_admin_buscar_usuario_por_nombre_usuario(create_jwt):
    response = create_jwt.get("/search_user?buscar=worker")

    data_html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "/usuario_detalles/2" in data_html 

def test_admin_crear_usuario_con_imagen_exitosamente(create_jwt):
    imagen = Image.new("RGB", [100,100], color='red')

    image_bytes = io.BytesIO()
    imagen.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    datos_usuario = {'imagen': (image_bytes, "user.png"),'nombre': "juan",'contraseña': "pal123", 'confirmar': "pal123", 'acceso': 1,}

    response = create_jwt.post("/crear_usuario", data=datos_usuario)

    pool, cursor = instancia_conexion.iniciar_conexion()
    user,variable = usuarios.obtener_uno(4)
    obtenido = instancia_conexion.uno(cursor, user, variable)
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert obtenido[0] == 4

def test_admin_editar_usuario_exitosamente(create_jwt):
    imagen = Image.new("RGB", [100,100], color='green')

    image_bytes = io.BytesIO()
    imagen.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    datos_usuario = {'imagen': (image_bytes, "user.png"),'nombre': "juan",'contraseña': "pal123", 'confirmar': "pal123", 'acceso': 2,}

    response = create_jwt.post("/cambios_usuario/4", data=datos_usuario)

    pool, cursor = instancia_conexion.iniciar_conexion()
    user,variable = usuarios.obtener_uno(4)
    obtenido = instancia_conexion.uno(cursor, user, variable)
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert obtenido[7] == 2

def test_admin_no_puede_crear_usuario_con_nombre_usuario_duplicado(create_jwt):
    imagen = Image.new("RGB", [100,100], color='blue')

    image_bytes = io.BytesIO()
    imagen.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    datos_usuario = {'imagen': (image_bytes, "user.png"),'nombre': "juan",'contraseña': "pal123", 'confirmar': "pal123", 'acceso': 1,}

    response = create_jwt.post("/crear_usuario", data=datos_usuario)

    pool, cursor = instancia_conexion.iniciar_conexion()
    user,variable = usuarios.obtener_uno(5)
    obtenido = instancia_conexion.uno(cursor, user, variable)
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert obtenido == None

def test_admin_eliminar_usuario_exitosamente(create_jwt):
    response = create_jwt.post("/delete_usuario/4")

    pool, cursor = instancia_conexion.iniciar_conexion()
    user,variable = usuarios.obtener_uno(4)
    obtenido = instancia_conexion.uno(cursor, user, variable)
    instancia_conexion.cerrar_conexion(cursor, pool)

    assert response.status_code == 302
    assert obtenido[6] == True