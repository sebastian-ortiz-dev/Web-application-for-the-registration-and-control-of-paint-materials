from flask import Blueprint, render_template, request, redirect, flash, url_for
from middleware.auth import validation_jwt
from middleware.acces_level import validation_acces
from model_db.class_singlen import productor, proveedor, usuarios, instancia_conexion

# Rutas relacionadas a los productos, proveedores y perfiles inactivos
inactivos_route = Blueprint('inactivos', __name__, template_folder='templates')

@inactivos_route.route("/inactivos")
@validation_jwt
@validation_acces
def inactivos(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    texto = productor.listar_inactivo()
    producto = instancia_conexion.todos(cursor, texto)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('inactivos.html', productos=producto, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'], alerta=alerta)

# Ruta que renderiza la plantilla para eliminar un producto
@inactivos_route.route('/reintegrar_producto/<int:id>')
@validation_jwt
@validation_acces
def reintegrar_producto(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()  
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    producto, parametro = productor.obtener_uno(id) 
    producto_detalles = instancia_conexion.uno(cursor, producto, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('recuperar_producto.html', producto=producto_detalles, access_level=datos_usuario['nivel_acceso'], alerta=alerta, nombre=name, imagen=imagen_usuario)

@inactivos_route.route('/recuperar_producto/<int:id>', methods=['POST'])
@validation_jwt
@validation_acces
def recuperar_producto(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()  
    texto, parametro = productor.recuperar_producto(id)
    instancia_conexion.registrar(cursor, texto, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    if resultado:
        flash('El producto ha sido reintegrado')
        return redirect(url_for("inactivos.inactivos"))
    else:
        flash('Ha ocurrido un error al tratar de reintegrar el producto')
        return redirect(url_for("inactivos.reintegrar_producto", id=id))

# Ruta de barra de busqueda de productos inactivos
@inactivos_route.route('/busqueda_producto_inactivo')
@validation_jwt
@validation_acces
def busqueda_producto_inactivo(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()   
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    producto, parametro = productor.busqueda_productos_inactivo(filtro)
    resultado_busqueda = instancia_conexion.todos_parametros(cursor, producto, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('inactivos.html', productos=resultado_busqueda, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

@inactivos_route.route("/inactivos_proveedor")
@validation_jwt
@validation_acces
def inactivo_proveedor(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    texto = proveedor.listar_inactivo()
    proveedores = instancia_conexion.todos(cursor, texto)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('inactivos_proveedores.html', proveedores=proveedores, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'], alerta=alerta)

# Ruta para recuperar el proveedor
@inactivos_route.route('/reintegrar_proveedor/<int:id>')
@validation_jwt
@validation_acces
def reintegrar_proveedor(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    consulta, parametro = proveedor.obtener_uno(id)
    proveedores = instancia_conexion.uno(cursor, consulta, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('recuperar_proveedor.html', proveedor_obtenido=proveedores, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

@inactivos_route.route('/recuperar_proveedor/<int:id>', methods=['POST'])
@validation_jwt
@validation_acces
def recuperar_proveedor(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()    
    consulta, parametro = proveedor.recuperar_proveedor(id)
    instancia_conexion.registrar(cursor, consulta, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash("El proveedor ha sido reintegrado")
        return redirect(url_for('inactivos.inactivo_proveedor'))
    else:
        flash('Ha ocurrido un error al reintegrar el proveedor')
        return redirect(url_for('inactivos.reintegrar_proveedor', id=id))

# Ruta que busca los proveedores inactivos
@inactivos_route.route('/buscar_proveedor_inactivo')
@validation_jwt
@validation_acces
def busqueda_proveedor_inactivo(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad) 
    consulta, parametro = proveedor.busqueda_proveedor_inactivo(filtro)
    proveedores = instancia_conexion.todos_parametros(cursor, consulta, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('inactivos_proveedores.html', proveedores=proveedores, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

@inactivos_route.route("/inactivos_perfiles")
@validation_jwt
@validation_acces
def inactivo_perfil(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    texto = usuarios.listar_inactivo_perfil()
    perfiles = instancia_conexion.todos(cursor, texto)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('perfil_inactivo.html', usuarios=perfiles, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'], alerta=alerta)

@inactivos_route.route('/reintegrar_perfil/<int:id>')
@validation_jwt
@validation_acces
def reintegrar_perfil(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    usuario, parametro = usuarios.obtener_uno(id)
    perfiles = instancia_conexion.uno(cursor, usuario, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('recuperar_perfil.html', usuario=perfiles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta que reintegra el perfil a la aplicacion
@inactivos_route.route('/recuperar_perfil/<int:id>', methods=['POST'])
@validation_jwt
@validation_acces
def recuperar_perfil(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    usuario, parametro = usuarios.recuperar_usuario(id)
    instancia_conexion.registrar(cursor, usuario, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash("El perfil ha sido reintegrado")
        return redirect(url_for('inactivos.inactivo_perfil'))
    else:
        flash("Ha ocurrido un error al tratar de reintegrar el perfil")
        return redirect(url_for('inactivos.reintegrar_perfil', id=id))

# Ruta que busca los perfiles inactivos
@inactivos_route.route('/busqueda_perfiles_inactivo')
@validation_jwt
@validation_acces
def busqueda_perfil_inactivo(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    usuario, parametro = usuarios.busqueda_usuario_inactivo(filtro)
    perfiles = instancia_conexion.todos_parametros(cursor, usuario, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('perfil_inactivo.html', usuarios=perfiles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])