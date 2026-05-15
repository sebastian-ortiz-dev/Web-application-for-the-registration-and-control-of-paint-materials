from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from middleware.auth import validation_jwt
from secure.process_image import *
from secure.hash_password import Hash_password
from werkzeug.utils import secure_filename
from datetime import date
import os
from secure.file_secure import allowed_file
from model_db.conexion import Conexion
from model_db.model_class.model_usuario import Usuario
from model_db.model_class.model_acceso import Acceso
from model_db.model_class.model_producto import Producto
from model_db.model_class.model_listado import Tipo_listado

# Rutas relacionadas a los usuarios de la aplicacion web
usuario_route = Blueprint('usuario', __name__, template_folder='templates')

productor = Producto() 
acceso = Acceso()
usuario = Usuario()
listado = Tipo_listado()
hash = Hash_password()
instancia_conexion = Conexion()

# Ruta con la vista principal de los usuarios
@usuario_route.route('/usuarios')

@validation_jwt
def trabajadores_registrados(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    usuarios = usuario.listar()
    usuario_detalles = instancia_conexion.todos(cursor, usuarios)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('usuarios.html', usuarios=usuario_detalles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta con la vista con los filtros aplicados
@usuario_route.route('/usuarios_filtro/<int:categoria>')

@validation_jwt
def trabajadores_filtro(categoria, datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    filtro= listado.lista_usuario_filtro(categoria)
    usuario_detalles = instancia_conexion.todos(cursor, filtro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    if categoria == 1 or categoria == 2:
        return render_template('trabajador_admin.html', usuarios=usuario_detalles, alerta=alerta, categoria=categoria, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])
    else:
        return render_template('usuarios.html', usuarios=usuario_detalles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta con los detalles de un usuario seleccionado
@usuario_route.route('/usuario_detalles/<int:id>')

@validation_jwt
def usuario_detalles(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    usuarios, parametro = usuario.obtener_uno(id)
    usuario_detalles = instancia_conexion.uno(cursor, usuarios, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('detalles_usuario.html', usuario=usuario_detalles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta que renderiza la vista con el formulario para un nuevo usuario 
@usuario_route.route('/usuario_nuevo')

@validation_jwt
def usuario_nuevo(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    accesos = acceso.listar()
    niveles = instancia_conexion.todos(cursor, accesos)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('agregar_usuario.html', niveles=niveles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta que trae los datos y crea el usuario en la base de datos
@usuario_route.route('/crear_usuario', methods=['POST'])

@validation_jwt
def crear_usuario(datos_usuario):
    imagen = request.files['imagen']
    nombre = request.form['nombre']
    contraseña = request.form['contraseña']
    confirmar = request.form['confirmar']
    acceso = request.form['acceso']
    filename = None
    subcarpeta = 'perfil'
    if acceso == " ":
        flash("Eliga un perfil para el nuevo usuario")
        return redirect(url_for('usuario.usuario_nuevo'))

    if contraseña != confirmar: 
        flash('¡Error! Las claves no coinciden') 
        return redirect(url_for('usuario.usuario_nuevo'))
    
    if not image_verification(imagen):
        flash('Formato de imagen no permitido')
        return redirect(url_for('usuario.usuario_nuevo'))

    if imagen != "" and imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta,filename))
        archivo = generate_name_unique(filename)
        os.rename(os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta, filename), os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta, archivo))
    else:
        archivo = "usuario_defecto.png"

    contraseña = hash.create_hash(contraseña)
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    usuarios, parametro = usuario.create_usuario(nombre, contraseña, acceso, archivo, date.today())
    try:
        instancia_conexion.registrar(cursor, usuarios, parametro)
    except Exception as e:
        print(f"Error: {e}")
        flash("Error: El nombre de usuario ya existe")
        return redirect(url_for("usuario.usuario_nuevo"))
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    if resultado:
        flash('Usuario registrado exitosamente')
        return redirect(url_for('usuario.trabajadores_registrados'))
    else:
        flash('¡Error! ha ocurrido un error al registrar el nuevo usuario')
        return redirect(url_for('usuario.usuario_nuevo'))
    
# Ruta que renderiza la vista para editar un usuario
@usuario_route.route('/editar_usuario/<int:id>')

@validation_jwt
def editar_usuario(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    accesos = acceso.listar()
    niveles = instancia_conexion.todos(cursor, accesos)
    usuarios, parametro = usuario.obtener_uno(id)
    usuario_detalles = instancia_conexion.uno(cursor, usuarios, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('editar_usuario.html', usuario=usuario_detalles, alerta=alerta, niveles=niveles, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta que efectua los cambios del usuario en la base de datos
@usuario_route.route('/cambios_usuario/<int:id>', methods=['POST'])

@validation_jwt
def cambios_usuario(datos_usuario, id):
    imagen = request.files['imagen']
    nombre = request.form['nombre']
    contraseña = request.form['contraseña']
    confirmar = request.form['confirmar']
    acceso = request.form['acceso']
    filename = None
    subcarpeta = 'perfil'
    verification = True

    if contraseña != confirmar:
        flash('¡Error! Las contraseñas no coinciden')
        return redirect(url_for('usuario.editar_usuario', id=id))
    
    if imagen:
        verification = image_verification(imagen.read())

    if not verification:
        flash('Formato de imagen no permitido')
        return redirect(url_for('usuario.usuario_nuevo'))

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta,filename))
        archivo = generate_name_unique(filename)
        os.rename(os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta, filename), os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta, archivo))
    else:
        archivo = request.form.get('foto_actual')

    contraseña = hash.create_hash(contraseña)
    
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    usuarios, parametro = usuario.modificar_usuario(nombre, contraseña, acceso, archivo, id)
    try:
        instancia_conexion.registrar(cursor, usuarios, parametro)
    except Exception as e:
        print(f"Error: {e}")
        flash("Error: El nombre de usuario ya existe")
        return redirect(url_for('usuario.editar_usuario', id=id))
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash('Usuario modificado exitosamente')
        return redirect(url_for('usuario.trabajadores_registrados'))
    else:
        flash('¡Error! ha ocurrido un error al modificar el usuario')
        return redirect(url_for('usuario.editar_usuario', id=id))
    
# Ruta que renderiza la vista para eliminar el usuario
@usuario_route.route('/eliminar_usuario/<int:id>')

@validation_jwt
def eliminar_usuario(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    usuarios, parametro = usuario.obtener_uno(id)
    usuario_detalles = instancia_conexion.uno(cursor, usuarios, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('eliminar_usuario.html', usuario=usuario_detalles, alerta=alerta, nombre=name, imagen=imagen_usuario)

# Ruta que elimina el usuario en la base de datos (En realidad realiza un soft delete)
@usuario_route.route('/delete_usuario/<int:id>', methods=['POST'])

@validation_jwt
def delete_usuario(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    usuarios, parametro = usuario.eliminar_usuario(id)
    instancia_conexion.registrar(cursor, usuarios, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash("Perfil eliminado")
        return redirect(url_for('usuario.trabajadores_registrados'))
    else:
        flash("Ha ocurrido un error al tratar de eliminar el perfil")
        return redirect(url_for('usuario.eliminar_usuario', id=id))

# Ruta que efectua la busqueda mediante la entrada de la barra de busqueda
@usuario_route.route('/search_user')

@validation_jwt
def busqueda_usuario(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    usuarios, parametro = usuario.busqueda_usuario(filtro)
    usuario_detalles = instancia_conexion.todos_parametros(cursor, usuarios, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('usuarios.html', usuarios=usuario_detalles, alerta=alerta, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])

# Ruta que efectua la busqueda mediante la entrada de la barra de busqueda tomando en cuenta el filtro de nivel de acceso
@usuario_route.route('/search_user_access')

@validation_jwt
def busqueda_usuario_acceso(datos_usuario):
    filtro = (f'%{request.args['buscar']}%')
    categoria = request.args['acceso']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    usuarios, parametro = usuario.busqueda_usuario_acceso(filtro, categoria)
    usuario_detalles = instancia_conexion.todos_parametros(cursor, usuarios, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('trabajador_admin.html', usuarios=usuario_detalles, alerta=alerta, categoria=categoria, nombre=name, imagen=imagen_usuario, access_level=datos_usuario['nivel_acceso'])