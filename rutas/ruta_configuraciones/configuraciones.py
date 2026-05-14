from flask import Blueprint, render_template, request, redirect, flash, url_for
from secure.secure_login import login_requerido
from middleware.auth import *
from model_db.conexion import Conexion
from model_db.model_class.model_producto import Producto
from model_db.model_class.model_categoria import Categoria
from model_db.model_class.model_medida import Medida

# Rutas relacionadas a las configuraciones
configuracion_route = Blueprint('configuracion', __name__, template_folder='templates')

productor = Producto()
medida = Medida()
categoria = Categoria()
instancia_conexion = Conexion()

@configuracion_route.route("/configuracion")
@login_requerido
@validation_jwt
def configuracion(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    texto = medida.listar()
    medidas = instancia_conexion.todos(cursor, texto)
    texto2 = categoria.listar()
    categorias = instancia_conexion.todos(cursor, texto2)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('configuracion.html', medidas=medidas, categorias=categorias, nombre=name, imagen=imagen_usuario, alerta=alerta)

@configuracion_route.route("/agregar_categoria")
@login_requerido
@validation_jwt
def agregar_categoria(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('agregar_categoria.html', nombre=name, imagen=imagen_usuario, alerta=alerta)

@configuracion_route.route("/crear_categoria", methods=['POST'])
@login_requerido
@validation_jwt
def crear_categoria(datos_usuario):
    nombre_categoria = request.form['nombre']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    texto, parametro = categoria.crear(nombre_categoria)
    instancia_conexion.registrar(cursor, texto, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash('Categoria creada')
        return redirect(url_for("configuracion.configuracion"))
    else:
        flash("Ha ocurrido un error al registrar la categoria")
        return redirect(url_for("configuracion.agregar_categoria"))
    
@configuracion_route.route("/editar_categoria/<int:id>")
@login_requerido
@validation_jwt
def editar_categoria(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    texto, parametro = categoria.obtener_uno(id)
    categorias = instancia_conexion.uno(cursor, texto, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('editar_categoria.html', categoria=categorias, nombre=name, imagen=imagen_usuario, alerta=alerta)

@configuracion_route.route("/modificar_categoria/<int:id>", methods=['POST'])
@login_requerido
@validation_jwt
def modificar_categoria(datos_usuario, id):
    nombre = request.form['nombre']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    texto, parametro = categoria.modificar(nombre, id)
    instancia_conexion.registrar(cursor, texto, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash("Categoria modificada")
        return redirect(url_for("configuracion.configuracion"))
    else:
        flash("Error al realizar el cambio")
        return redirect(url_for("configuracion.editar_categoria", id=id))
    

@configuracion_route.route("/agregar_medida")
@login_requerido
@validation_jwt
def agregar_medida(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('agregar_medida.html', nombre=name, imagen=imagen_usuario, alerta=alerta)

@configuracion_route.route("/editar_medida/<int:id>")
@login_requerido
@validation_jwt
def editar_medida(datos_usuario, id):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    texto, parametro = medida.obtener_uno(id)
    medidas = instancia_conexion.uno(cursor, texto, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('editar_medida.html', medida=medidas, nombre=name, imagen=imagen_usuario, alerta=alerta)

@configuracion_route.route("/modificar_medida/<int:id>", methods=['POST'])
@login_requerido
@validation_jwt
def modificar_medida(id, datos_usuario):
    nombre = request.form['nombre']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    texto, parametro = medida.modificar(nombre, id)
    instancia_conexion.registrar(cursor, texto, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash("Categoria modificada")
        return redirect(url_for("configuracion.configuracion"))
    else:
        flash("Error al realizar el cambio")
        return redirect(url_for("configuracion.editar_medida", id=id))


@configuracion_route.route("/crear_medida", methods=['POST'])
@login_requerido
@validation_jwt
def crear_medida(datos_usuario):
    nombre_medida = request.form['nombre']
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    texto, parametro = medida.crear(nombre_medida)
    instancia_conexion.registrar(cursor, texto, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash('Medida creada')
        return redirect(url_for("configuracion.configuracion"))
    else:
        flash("Ha ocurrido un error al registrar la medida")
        return redirect(url_for("configuracion.agregar_medida"))