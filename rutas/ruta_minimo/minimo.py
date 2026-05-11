from flask import Blueprint, render_template, session, request
from secure.secure_login import login_requerido
from middleware.auth import validation_jwt
from model_db.conexion import Conexion
from model_db.model_class.model_producto import Producto
from model_db.model_class.model_listado import Tipo_listado
from model_db.model_class.model_proveedor import Proveedor
from model_db.model_class.model_categoria import Categoria
from secure.obtener_proveedores import get_producto_id
from secure.sin_movimientos import limpiar

# Rutas relacionadas al inventario con alerta a en stock minimo de la aplicacion web

minimo_route = Blueprint('minimo', __name__, template_folder='templates')

productor = Producto() 
proveedor = Proveedor()
listado = Tipo_listado()
categorias = Categoria()
@minimo_route.route('/alerta')
@login_requerido
@validation_jwt
def alerta(datos_usuario):
    instancia_conexion = Conexion()
    cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto = productor.listar_minimo()
    productos_minimo = instancia_conexion.todos(cursor, producto)
    categoria = instancia_conexion.todos(cursor, categorias.listar())
    instancia_conexion.cerrar_conexion(cursor)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('minimo.html', productos=productos_minimo, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario)

@minimo_route.route('/tipo_minimo/<int:categoria>')
@login_requerido
@validation_jwt
def filtro(datos_usuario, categoria):
    instancia_conexion = Conexion()
    cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    tipo, parametro = listado.listar_minimo(categoria)
    producto = instancia_conexion.todos_parametros(cursor, tipo, parametro)
    categoria_todo = instancia_conexion.todos(cursor, categorias.listar())
    instancia_conexion.cerrar_conexion(cursor)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('minimo_filtro.html', productos=producto, categorias_todas=categoria_todo, alerta=alerta, categoria=categoria, nombre=name, imagen=imagen_usuario)

# Filtro que lista cada producto minimo segun su proveedor
@minimo_route.route('/por_proveedores_minimo')
@login_requerido
@validation_jwt
def por_proveedores(datos_usuario):
    instancia_conexion = Conexion()
    cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto = productor.listar_minimo()
    productos_minimo = instancia_conexion.todos(cursor, producto)
    categoria = instancia_conexion.todos(cursor, categorias.listar())
    if len(productos_minimo) != 0:
        id_productos = get_producto_id(productos_minimo)
        proveedores, parametro = productor.obtener_proveedores(tuple(id_productos))
        proveedores_id = instancia_conexion.todos_parametros(cursor, proveedores, parametro)
        limpio = limpiar(proveedores_id)
        lista_id, parametro = proveedor.obtener_proveedores(tuple(limpio))
        set_proveedores = instancia_conexion.todos_parametros(cursor, lista_id, parametro)
    else:
        producto = False
        set_proveedores = False
    instancia_conexion.cerrar_conexion(cursor)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('listar_minimo_proveedor.html', productos=productos_minimo, categoria=categoria, alerta=alerta, proveedores=set_proveedores, nombre=name, imagen=imagen_usuario)

# Ruta de barra de busqueda de productos
@minimo_route.route('/search_bar_minimo')
@login_requerido
@validation_jwt
def busqueda_minimo(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    instancia_conexion = Conexion()
    cursor = instancia_conexion.iniciar_conexion()   
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto, parametro = productor.busqueda_productos_minimo(filtro)
    resultado_busqueda = instancia_conexion.todos_parametros(cursor, producto, parametro)
    categoria = instancia_conexion.todos(cursor, categorias.listar())
    instancia_conexion.cerrar_conexion(cursor)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('minimo.html', productos=resultado_busqueda, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario)

# Barra de busqueda pero con filtro aplicado
@minimo_route.route('/filtro_minimum_search')
@login_requerido
@validation_jwt
def minimo_filtro_busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    categoria = request.args['categoria']
    instancia_conexion = Conexion()
    cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)  
    producto, parametro = productor.busqueda_minimo_categoria(filtro, categoria)
    resultado_busqueda = instancia_conexion.todos_parametros(cursor, producto, parametro)
    categoria_todo = instancia_conexion.todos(cursor, categorias.listar())
    instancia_conexion.cerrar_conexion(cursor)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('minimo_filtro.html',  productos=resultado_busqueda, categorias_todas=categoria_todo, alerta=alerta, categoria=categoria, nombre=name, imagen=imagen_usuario)

# Barra de busqueda que lista los productos minimos segun su distribuidor
@minimo_route.route('/por_proveedores_search_minimo')
@login_requerido
@validation_jwt
def producto_minimo_proveedores_busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    instancia_conexion = Conexion()
    cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)  
    producto, parametro = productor.busqueda_productos_minimo(filtro)
    resultado_busqueda = instancia_conexion.todos_parametros(cursor, producto, parametro)
    categoria = instancia_conexion.todos(cursor, categorias.listar())
    if len(resultado_busqueda) != 0:
        id_productos = get_producto_id(resultado_busqueda)
        proveedores, parametro = productor.obtener_proveedores(tuple(id_productos))
        proveedores_id = instancia_conexion.todos_parametros(cursor, proveedores, parametro)
        limpio = limpiar(proveedores_id)
        lista_id, parametro = proveedor.obtener_proveedores(tuple(limpio))
        set_proveedores = instancia_conexion.todos_parametros(cursor, lista_id, parametro)
    else:
        producto = False
        set_proveedores = False
    instancia_conexion.cerrar_conexion(cursor)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('minimo_producto_proveedor.html', productos=resultado_busqueda, categoria=categoria, alerta=alerta, proveedores=set_proveedores, nombre=name, imagen=imagen_usuario)