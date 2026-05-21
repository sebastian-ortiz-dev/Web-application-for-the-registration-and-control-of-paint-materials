from flask import Blueprint, render_template
from middleware.auth import validation_jwt
from model_db.class_singlen import productor, historial, proveedor, usuarios, instancia_conexion
from secure.sin_movimientos import dia
from secure.sin_movimientos import sin_movimiento


# Rutas relacionadas a la vista general de la aplicacion web
dashboard_route = Blueprint('dashboard', __name__, template_folder='templates')

# Ruta con la vista general del negocio
@dashboard_route.route('/principal')
@validation_jwt
def dashboard(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto = instancia_conexion.todos(cursor, productor.obtener_cantidad_productos())
    productos_movimientos = instancia_conexion.todos(cursor, productor.obtener_cantidad_sin_movimientos())
    devoluciones, parametro = historial.contar_devoluciones()
    total_devoluciones = instancia_conexion.todos_parametros(cursor, devoluciones, parametro)
    devoluciones, parametro = historial.contar_devoluciones_total_bs()
    total_devoluciones_bs = instancia_conexion.todos_parametros(cursor, devoluciones, parametro)
    entradas, parametro = historial.contar_entradas()
    total_entradas = instancia_conexion.todos_parametros(cursor, entradas, parametro)
    entradas, parametro = historial.contar_entradas_total_bs()
    total_entradas_bs = instancia_conexion.todos_parametros(cursor, entradas, parametro)
    salidas, parametro = historial.contar_salidas()
    total_salidas = instancia_conexion.todos_parametros(cursor, salidas, parametro)
    salidas, parametro = historial.contar_salidas_total_bs()
    total_salidas_bs = instancia_conexion.todos_parametros(cursor, salidas, parametro)
    ajuste, parametro = historial.contar_ajustes()
    total_ajustes = instancia_conexion.todos_parametros(cursor, ajuste, parametro)
    ajuste_aumento, parametro = historial.contar_ajustes_total_aumento()
    total_ajuste_aumento = instancia_conexion.todos_parametros(cursor, ajuste_aumento, parametro)
    ajuste_disminucion, parametro = historial.contar_ajustes_total_disminucion()
    total_ajuste_disminucion = instancia_conexion.todos_parametros(cursor, ajuste_disminucion, parametro)
    texto = productor.contar_productos_inactivo()
    texto2 = proveedor.contar_inactivo()
    texto3 = usuarios.contar_perfil_inactivo()
    num_producto = instancia_conexion.todos(cursor, texto)
    num_proveedor = instancia_conexion.todos(cursor, texto2)
    num_perfil = instancia_conexion.todos(cursor, texto3)
    num_total_inactivo = num_producto[0][0] + num_proveedor[0][0] + num_perfil[0][0]
    producto_id = instancia_conexion.todos(cursor, productor.listar_id())
    hoy, hace_30 = dia()
    texto, parametro = historial.listar_hace_30(hoy, hace_30)
    movimientos_id = instancia_conexion.todos_parametros(cursor, texto, parametro)
    no_movimientos = sin_movimiento(producto_id[0][0], movimientos_id[0][0])
    if len(no_movimientos) != 0:
        query, parametros = productor.modificar_cantidad_sin_movimientos(tuple(no_movimientos))
        instancia_conexion.registrar(cursor, query, parametros)
        instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('principal.html', productos=producto, movimiento=num_total_inactivo, no_movimiento=productos_movimientos,  ids=no_movimientos, devoluciones=total_devoluciones, entradas=total_entradas, salidas=total_salidas, devoluciones_bs=total_devoluciones_bs, entradas_bs=total_entradas_bs, salidas_bs=total_salidas_bs, ajuste=total_ajustes, ajuste_aumento=total_ajuste_aumento, ajuste_disminucion=total_ajuste_disminucion, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])