from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from middleware.auth import validation_jwt
from middleware.acces_level import validation_acces
from model_db.conexion import Conexion
from model_db.model_class.model_proveedor import Proveedor
from model_db.model_class.model_producto import Producto
from model_db.model_class.model_listado import Tipo_listado
from datetime import date

# Rutas relacionadas a los proveedores de la aplicacion web
proveedor_route = Blueprint('proveedor', __name__, template_folder='templates')

productor = Producto() 
proveedor = Proveedor()
listado = Tipo_listado()
instancia_conexion = Conexion()
# Ruta con la vista principal con los proveedores
@proveedor_route.route('/proveedores')
@validation_jwt
def proveedores(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    consulta = proveedor.listar()
    proveedores = instancia_conexion.todos(cursor, consulta)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('proveedores.html', lista_proveedores=proveedores, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

@proveedor_route.route('/listado_proveedores/<int:categoria>')
@validation_jwt
def tipo_listado(datos_usuario, categoria):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    tipo = listado.lista_proveedor(categoria)
    proveedores = instancia_conexion.todos(cursor, tipo)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('proveedores.html', lista_proveedores=proveedores, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta con la vista para crear un nuevo proveedor
@proveedor_route.route('/nuevo_proveedor')
@validation_jwt
@validation_acces
def proveedor_nuevo(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('agregar_proveedor.html', alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta para obtener los datos y guardarlos en la DB
@proveedor_route.route('/crear_proveedor', methods=['POST'])
@validation_jwt
@validation_acces
def crear_proveedor(datos_usuario):
    nombre = request.form['nombre']
    correo = request.form['correo']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    rif = request.form['rif']

    pool_db, cursor = instancia_conexion.iniciar_conexion()
    consulta, parametros = proveedor.create_proveedor(nombre, correo, direccion, telefono, rif, date.today())
    instancia_conexion.registrar(cursor, consulta, parametros) 
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    if resultado:
        flash('Proveedor registrado exitosamente')
        return redirect(url_for('proveedor.proveedores'))
    else:
        flash('¡Error! ha ocurrido un error al registrar al nuevo proveedor')
        return redirect(url_for('proveedor.proveedor_nuevo'))
    
# Ruta para mostrar la vista para editar un proveedor
@proveedor_route.route('/edit_proveedor/<int:id>')
@validation_jwt
@validation_acces
def editar_proveedor(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    consulta, parametro = proveedor.obtener_uno(id)
    proveedores = instancia_conexion.uno(cursor, consulta, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    if not proveedores:
        abort(404)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('editar_proveedor.html', proveedor_obtenido=proveedores, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta para obtener los datos y guardas los cambios
@proveedor_route.route('/cambios_proveedor/<int:id>', methods=['POST'])
@validation_jwt
@validation_acces
def cambio_proveedor(datos_usuario, id):
    nombre = request.form['nombre']
    correo = request.form['correo']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    rif = request.form['rif']

    pool_db, cursor = instancia_conexion.iniciar_conexion()
    modifica, parametro = proveedor.modificar_proveedor(id, nombre, correo, direccion, telefono, rif)
    instancia_conexion.registrar(cursor, modifica, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    if resultado:
        flash('Proveedor modificado')
        return redirect(url_for('proveedor.proveedores'))
    else:
        flash('¡Error! ha ocurrido un error al modificar al proveedor')
        return redirect(url_for('proveedor.editar_proveedor', id=id))

# Ruta para mostrar el proveedor a "eliminar"
@proveedor_route.route('/eliminar_proveedor/<int:id>')
@validation_jwt
@validation_acces
def eliminar_proveedor(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad= productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    consulta, parametro = proveedor.obtener_uno(id)
    proveedores = instancia_conexion.uno(cursor, consulta, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('eliminar_proveedor.html', proveedor_obtenido=proveedores, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta para eliminar el proveedor de la DB
@proveedor_route.route('/delete_proveedor/<int:id>', methods=['POST'])
@validation_jwt
@validation_acces
def delete_proveedor(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()    
    consulta, parametro = proveedor.eliminar_proveedor(id)
    instancia_conexion.registrar(cursor, consulta, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash("Proveedor eliminado")
        return redirect(url_for('proveedor.proveedores'))
    else:
        flash("Ocurrio un error al tratar de eliminar al proveedor")
        return redirect(url_for('proveedor.eliminar_proveedor', id=id))

# Ruta que hace uso de la barra de busqueda
@proveedor_route.route('/buscar_proveedor')
@validation_jwt
def barra_busqueda(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    consulta, parametro = proveedor.busqueda_proveedor(filtro) 
    proveedores = instancia_conexion.todos_parametros(cursor, consulta, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('proveedores.html', lista_proveedores=proveedores, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])