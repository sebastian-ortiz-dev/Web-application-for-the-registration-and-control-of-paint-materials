from flask import Blueprint, render_template, request
from middleware.auth import validation_jwt
from model_db.class_singlen import productor, proveedor, category, listado, instancia_conexion
from utils.obtener_proveedores import get_producto_id
from utils.sin_movimientos import limpiar

# Rutas relacionadas a los productos sin movimientos de la aplicacion web
sin_movimiento_route = Blueprint('sin_movimiento', __name__, template_folder='templates')

# ruta con la vista de los productos sin movimientos en los ultimos treinta dias
@sin_movimiento_route.route('/sin_movimientos')
@validation_jwt
def no_movimientos(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    productos = productor.listar_sin_movimiento()
    producto = instancia_conexion.todos(cursor, productos)
    categoria = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('sin_movimientos.html', productos=producto, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Lista por categoria 
@sin_movimiento_route.route('/tipo_listado/<int:categoria>')
@validation_jwt
def listado_filtro(datos_usuario, categoria):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    tipo, parametro = listado.listar_no_movimientos(categoria)
    producto = instancia_conexion.todos_parametros(cursor, tipo, parametro)
    categoria_todo = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('sin_movimientos_filtro.html', productos=producto, set_categoria=categoria_todo, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# lista por proveedores los productos relacionados a sus proveedores
@sin_movimiento_route.route('/por_proveedores_no_movimientos')
@validation_jwt
def sin_movimiento_proveedores(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    productos = productor.listar_sin_movimiento()
    producto = instancia_conexion.todos(cursor, productos)
    categoria = instancia_conexion.todos(cursor, category.listar())
    if len(producto) != 0:
        id_productos = get_producto_id(producto)
        proveedores, parametro = productor.obtener_proveedores(tuple(id_productos))
        proveedores_id = instancia_conexion.todos_parametros(cursor, proveedores, parametro)
        limpio = limpiar(proveedores_id)
        lista_id, parametro = proveedor.obtener_proveedores(tuple(limpio))
        proveedores = instancia_conexion.todos_parametros(cursor, lista_id, parametro)
    else:
        producto = False
        proveedores = False
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('por_proveedores.html', productos=producto, categoria=categoria, alerta=alerta, proveedores=proveedores, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta de barra de busqueda de productos sin movimientos
@sin_movimiento_route.route('/search_bar_no_movimientos')
@validation_jwt
def busqueda_no_movimientos(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()   
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto, parametro = productor.busqueda_productos_sin_movimiento(filtro)
    resultado_busqueda = instancia_conexion.todos_parametros(cursor, producto, parametro)
    categoria = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('sin_movimientos.html', productos=resultado_busqueda, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Barra de busqueda pero con filtro aplicado
@sin_movimiento_route.route('/filtro_no_movientos_search')
@validation_jwt
def movimientos_filtro_busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    categoria = request.args['categoria']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)  
    productos, parametro = productor.busqueda_productos_categoria_sin_movimientos(filtro, categoria)
    producto = instancia_conexion.todos_parametros(cursor, productos, parametro)
    categoria_todo = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('sin_movimientos_filtro.html',  productos=producto, set_categoria=categoria_todo, alerta=alerta, categoria=categoria, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Barra de busqueda que lista los productos minimos segun su distribuidor
@sin_movimiento_route.route('/por_proveedores_search_sin_movimiento')
@validation_jwt
def proveedores_sin_movimiento_busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto, parametro = productor.busqueda_productos_sin_movimiento(filtro)
    resultado_busqueda = instancia_conexion.todos_parametros(cursor, producto, parametro)
    categoria = instancia_conexion.todos(cursor, category.listar())
    if len(resultado_busqueda) != 0:
        id_productos = get_producto_id(resultado_busqueda)
        proveedores, parametro = productor.obtener_proveedores(tuple(id_productos))
        proveedores_id = instancia_conexion.todos_parametros(cursor, proveedores, parametro)
        limpio = limpiar(proveedores_id)
        lista_id, parametro = proveedor.obtener_proveedores(tuple(limpio))
        proveedores = instancia_conexion.todos_parametros(cursor, lista_id, parametro)
    else:
        resultado_busqueda = False
        proveedores = False
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('producto_proveedor_sin_movimiento.html', productos=resultado_busqueda, categoria=categoria, alerta=alerta, proveedores=proveedores, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])