from flask import Blueprint, render_template, request
from secure.secure_login import login_requerido
from middleware.auth import validation_jwt
from model_db.conexion import Conexion
from model_db.model_class.model_historial import Historia_Movimientos
from model_db.model_class.model_producto import Producto
from model_db.model_class.model_listado import Tipo_listado

# Rutas relacionadas al historial de movimientos de la aplicacion web
historial_route = Blueprint('historial', __name__, template_folder='templates')

productor = Producto() 
listado = Tipo_listado()
historial = Historia_Movimientos()
instancia_conexion = Conexion()
# Ruta que lista todos los movimientos que se hacen
@historial_route.route('/historia')
@login_requerido
@validation_jwt
def historial_movimientos(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    consulta, parametro = historial.listar()
    movimientos = instancia_conexion.todos_parametros(cursor, consulta, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('historial.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimientos)

# Ruta que lista todos los movimientos que se hacen
@historial_route.route('/historia_filtro/<int:categoria>')
@login_requerido
@validation_jwt
def historial_movimientos_filtro(datos_usuario, categoria):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)    
    tipo, parametro = listado.lista_historial_filtro(categoria)
    movimientos = instancia_conexion.todos_parametros(cursor, tipo, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('historial_filtro.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimientos, categoria=categoria)

# Ruta que lista el resultado de la busqueda de movimientos en intervalos de tiempo
@historial_route.route('/historial_intervalo')
@login_requerido
@validation_jwt
def historial_intervalo(datos_usuario):
    desde = request.args['desde']
    hasta = request.args['hasta']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    if desde == '' or hasta == '':
        movimientos = []
    else:
        query, parametro = historial.listar_intervalos(desde, hasta)
        movimientos = instancia_conexion.todos_parametros(cursor, query, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('historial_intervalos.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimientos, desde=desde, hasta=hasta)

# Ruta que lista el resultado de la busqueda de movimientos en intervalos con tipo de movimiento
@historial_route.route('/historial_intervalo_categoria')
@login_requerido
@validation_jwt
def historial_intervalo_categoria(datos_usuario):
    desde = request.args['desde']
    hasta = request.args['hasta']
    categoria = int(request.args['categoria'])
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    if desde == '' or hasta == '':
        movimientos = []
    else:
        query, parametro = historial.lista_historial_filtro_intervalo(categoria, desde, hasta)
        movimientos = instancia_conexion.todos_parametros(cursor, query, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('historial_intervalos_categoria.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimientos, desde=desde, hasta=hasta, categoria=categoria)

# Ruta que lista el resultado de la busqueda de movimientos
@historial_route.route('/historia_search')
@login_requerido
@validation_jwt
def historial_busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    consulta, parametro = historial.busqueda_historial(filtro)
    movimientos = instancia_conexion.todos_parametros(cursor, consulta, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('historial.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimientos)

# Ruta que lista el resultado de la busqueda de movimientos segun el tipo de listado
@historial_route.route('/historia_search_filtro')
@login_requerido
@validation_jwt
def historial_busqueda_filtro(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    categoria = int(request.args['categoria'])
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    consulta, parametro = historial.busqueda_historial_filtrado_dias(filtro, categoria)
    movimientos = instancia_conexion.todos_parametros(cursor, consulta, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('historial_filtro.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimientos, categoria=categoria)

# Ruta que lista el resultado de la busqueda de movimientos segun el intervalo
@historial_route.route('/historia_search_intervalo')
@login_requerido
@validation_jwt
def historial_busqueda_intervalo(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    desde = request.args['desde']
    hasta = request.args['hasta']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    if desde == '' or hasta == '':
        movimientos = []
    else:
        query, parametro = historial.busqueda_historial_intervalos(filtro, desde, hasta)
        movimientos = instancia_conexion.todos_parametros(cursor, query, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('historial_intervalos.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimientos, desde=desde, hasta=hasta)

# Ruta que lista el resultado de la busqueda de movimientos segun el intervalo tomando en cuenta el tipo de movimiento
@historial_route.route('/historia_search_intervalo_categoria')
@login_requerido
@validation_jwt
def historial_busqueda_intervalo_categoria(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    desde = request.args['desde']
    hasta = request.args['hasta']
    categoria = int(request.args['categoria'])
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    if desde == '' or hasta == '':
        movimientos = []
    else:
        query, parametro = historial.busqueda_historial_intervalos_Categoria(filtro, desde, hasta, categoria)
        movimientos = instancia_conexion.todos_parametros(cursor, query, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('historial_intervalos_categoria.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimientos, desde=desde, hasta=hasta, categoria=categoria)