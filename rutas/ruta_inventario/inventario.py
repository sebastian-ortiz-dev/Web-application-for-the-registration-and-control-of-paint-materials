from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from middleware.auth import validation_jwt
from middleware.acces_level import validation_acces
from secure.process_image import image_verification
from werkzeug.utils import secure_filename
from datetime import date
import os
from secure.file_secure import allowed_file
from utils.obtener_proveedores import get_producto_id
from utils.sin_movimientos import limpiar
from model_db.class_singlen import productor, proveedor, category, medida, listado, instancia_conexion

# Rutas relacionadas al inventario de la aplicacion web
inventario_route = Blueprint('inventario', __name__, template_folder='templates')


# Ruta que lista los productos con su proveedor, esta es la vista del Administrador
@inventario_route.route('/')
@validation_jwt
def index(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()   
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto = instancia_conexion.todos(cursor, productor.listar())
    categoria = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('index.html', productos=producto, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta que lista los productos con su distribuidor, esta es la vista del Trabajador
@inventario_route.route('/trabajador')
@validation_jwt
def trabajador(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto = instancia_conexion.todos(cursor, productor.listar())
    categoria = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('trabajador.html', productos=producto, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Lista por categoria 
@inventario_route.route('/tipo/<int:categoria>')
@validation_jwt
def tipo_listado(datos_usuario, categoria):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    texto, parametro = listado.listar(categoria)
    producto = instancia_conexion.todos_parametros(cursor, texto, parametro)
    categoria_todas = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('productos_filtro.html', productos=producto, set_categoria=categoria_todas, alerta=alerta, categoria=categoria, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Busqueda por filtro
@inventario_route.route('/filtro_search')
@validation_jwt
def producto_filtro_busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    categoria = request.args['categoria']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    texto, parametro = productor.busqueda_productos_categoria(filtro, categoria)
    producto = instancia_conexion.todos_parametros(cursor, texto, parametro)
    categoria_todas = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('productos_filtro.html',  productos=producto, set_categoria=categoria_todas, alerta=alerta, categoria=categoria, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Filtro que lista cada producto segun su proveedor (En un futuro optimizar)
@inventario_route.route('/por_proveedores')
@validation_jwt
def producto_proveedores(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()    
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    producto = instancia_conexion.todos(cursor, productor.listar())
    categoria = instancia_conexion.todos(cursor, category.listar())
    if len(producto) != 0:
        # mejorar, se puede usar un set y restarlo para obtener los proveedores sin necesidad de un for en la linea 97
        id_productos = get_producto_id(producto)
        proveedores, parametro = productor.obtener_proveedores(tuple(id_productos))
        proveedores_id = instancia_conexion.todos_parametros(cursor, proveedores, parametro)
        limpio = limpiar(proveedores_id)
        lista_id, parametro = proveedor.obtener_proveedores(tuple(limpio))
        set_proveedores = instancia_conexion.todos_parametros(cursor, lista_id, parametro)
    else:
        producto = False
        set_proveedores = False
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('por_proveedor_producto.html', productos=producto, categoria=categoria, alerta=alerta, proveedores=set_proveedores, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Barra de busqueda que lista el producto segun su proveedor
@inventario_route.route('/por_proveedores_search')
@validation_jwt
def producto_proveedores_busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    texto, parametro = productor.busqueda_productos(filtro)  
    producto = instancia_conexion.todos_parametros(cursor, texto, parametro)
    categoria = instancia_conexion.todos(cursor, category.listar())
    if len(producto) != 0:
        id_productos = get_producto_id(producto)
        proveedores, parametro = productor.obtener_proveedores(tuple(id_productos))
        proveedores_id = instancia_conexion.todos_parametros(cursor, proveedores, parametro)
        limpio = limpiar(proveedores_id)
        lista_id, parametro = proveedor.obtener_proveedores(tuple(limpio))
        set_proveedores = instancia_conexion.todos_parametros(cursor, lista_id, parametro)
    else:
        producto = False
        set_proveedores = False
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('por_producto_buscado.html', productos=producto, categoria=categoria, alerta=alerta, proveedores=set_proveedores, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])
    
# Ruta que renderiza la plantilla con los datos del producto a editar
@inventario_route.route('/editar/<int:id>')
@validation_jwt
@validation_acces
def editar(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()    
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    producto, parametro = productor.obtener_uno(id) 
    producto_detalles = instancia_conexion.uno(cursor, producto, parametro)
    proveedores = instancia_conexion.todos(cursor, proveedor.listar_varios())
    categoria = instancia_conexion.todos(cursor, category.listar())
    medidas = instancia_conexion.todos(cursor, medida.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('editar_producto.html', producto=producto_detalles, set_proveedores=proveedores, categorias=categoria, medidas=medidas, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta que contiene las consultas SQL y los datos para hacer los cambios para editar el producto
@inventario_route.route('/cambios_producto/<int:id>', methods=['POST'])
@validation_jwt
@validation_acces
def cambios_hecho(datos_usuario, id):
    imagen = request.files['imagen']
    nombre = request.form['nombre']
    detalles = request.form['detalles']
    precio = request.form['precio']
    cantidad = request.form['existencia']
    distribuidor = request.form['distribuidor']
    medida = request.form['medida']
    categoria = request.form['categoria']
    cantidad_minima = request.form['minima']
    filename = None
    subcarpeta = 'productos'
    verification = True

    if imagen:
        verification = image_verification(imagen.read())

    if not verification:
        flash('Formato de imagen no permitido')
        return redirect(url_for('inventario.editar', id=id))

    if distribuidor == "" or categoria == "" or medida == "":
        flash('¡Error! Complete todos los campos')
        return redirect(url_for('inventario.editar', id=id))

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta,filename))
    else:
        filename = request.form.get('foto_actual')
   
    pool_db, cursor = instancia_conexion.iniciar_conexion()    
    producto, parametro = productor.modificar_producto(id, nombre, detalles, precio, cantidad, date.today(), filename, distribuidor, categoria, cantidad_minima, medida)
    instancia_conexion.registrar(cursor, producto, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    if resultado:
        flash('Producto modificado exitosamente')
        if datos_usuario['nivel_acceso'] == 'Administrador':
            return redirect(url_for('inventario.index'))
        else:
            return redirect(url_for('inventario.trabajador'))
    else:
        flash('¡Error! ha ocurrido un error al modificar el producto')
        return redirect(url_for('inventario.editar', id=id))

# Ruta que renderiza la plantilla para eliminar un producto
@inventario_route.route('/eliminar/<int:id>')
@validation_jwt
@validation_acces
def eliminar(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()  
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    producto, parametro = productor.obtener_uno(id) 
    producto_detalles = instancia_conexion.uno(cursor, producto, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('eliminar_producto.html', producto=producto_detalles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta que elimina logicamente el producto de la base de datos
@inventario_route.route('/delete_producto/<int:id>', methods=['POST'])
@validation_jwt
@validation_acces
def delete_producto(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()  
    producto, parametro = productor.eliminar_producto(id) 
    instancia_conexion.registrar(cursor, producto, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash("Producto eliminado correctamente")
        if datos_usuario['nivel_acceso'] == 'Administrador':
            return redirect(url_for('inventario.index'))
        else:
            return redirect(url_for('inventario.trabajador'))
    else:
        flash('¡Error! ha ocurrido un error al tratar de eliminar el producto')
        return redirect(url_for('inventario.eliminar', id=id))

# Ruta que renderiza una plantilla con los detalles completos del producto
@inventario_route.route('/detalles/<int:id>')
@validation_jwt
def detalles(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()   
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)  
    producto, parametro = productor.obtener_uno(id)
    producto_detalles = instancia_conexion.uno(cursor, producto, parametro)
    print(producto_detalles)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('detalle.html', producto=producto_detalles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta de barra de busqueda de productos
@inventario_route.route('/search_bar')
@validation_jwt
def busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()   
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    producto, parametro = productor.busqueda_productos(filtro)
    resultado_busqueda = instancia_conexion.todos_parametros(cursor, producto, parametro)
    categoria = instancia_conexion.todos(cursor, category.listar())
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    if datos_usuario['nivel_acceso'] == "Administrador":
        return render_template('index.html', productos=resultado_busqueda, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])
    else:
        return render_template('trabajador.html', productos=resultado_busqueda, categoria=categoria, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])