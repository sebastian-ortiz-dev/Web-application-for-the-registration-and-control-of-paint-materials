from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from secure.secure_login import login_requerido
from middleware.auth import validation_jwt
from secure.process_image import *
from werkzeug.utils import secure_filename
from datetime import date, datetime
import os

from secure.file_secure import allowed_file
from model_db.conexion import Conexion
from model_db.model_class.model_movimientos import Movimientos
from model_db.model_class.model_producto import Producto
from model_db.model_class.model_proveedor import Proveedor
from model_db.model_class.model_historial import Historia_Movimientos
from model_db.model_class.model_categoria import Categoria
from model_db.model_class.model_medida import Medida

# Rutas relacionadas a los movimientos de la aplicacion web
movimiento_route = Blueprint('movimiento', __name__, template_folder='templates')

productor = Producto() 
proveedor = Proveedor()
categorias = Categoria()
medida = Medida()
movimientos = Movimientos()
historial = Historia_Movimientos()
instancia_conexion = Conexion()

# Ruta que lista la vista principal de los movimientos
@movimiento_route.route('/movimiento')
@login_requerido
@validation_jwt
def movimiento(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    movimiento = movimientos.listar()
    movimiento_todo = instancia_conexion.todos(cursor, movimiento)
    productos = productor.listar_necesario()
    producto = instancia_conexion.todos(cursor, productos)
    varios = proveedor.listar_varios()
    proveedores = instancia_conexion.todos(cursor, varios)
    categoria_lista = categorias.listar()
    categoria = instancia_conexion.todos(cursor, categoria_lista)
    medidas_consulta = medida.listar()
    medidas = instancia_conexion.todos(cursor, medidas_consulta)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    imagen_usuario = datos_usuario['imagen_usuario']  
    name = datos_usuario['usuario_nombre']
    return render_template('movimiento.html', nombre=name, imagen=imagen_usuario, alerta=alerta, movimiento=movimiento_todo, productos=producto, distribuidores=proveedores, categorias=categoria, medidas=medidas)

# Ruta que registra una entrada en la DB de un producto existente
@movimiento_route.route('/registrar_entrada_existente', methods=["POST"])
@login_requerido
@validation_jwt
def registrar_entrada(datos_usuario):
    tipo_movimiento = 1
    motivo = "Entrada de producto"
    producto = request.form['producto']
    cantidad = request.form['cantidad_entrada']
        
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    productos, parametro = productor.obtener_cantidad(producto)
    existencia = instancia_conexion.uno(cursor, productos, parametro)
    cantidad_total = int(existencia[0]) + int(cantidad)
    productos_modificado, parametros = productor.modifica_cantidad(producto, cantidad_total)
    instancia_conexion.registrar(cursor, productos_modificado, parametros)
    recupera, datos = productor.obtener_uno(producto)
    recuperar_producto = instancia_conexion.uno(cursor, recupera, datos)
    registrar_movimiento, parametro = historial.movimiento(recuperar_producto[0], cantidad, datetime.now(), session['id_usuario'], motivo, tipo_movimiento)
    instancia_conexion.registrar(cursor, registrar_movimiento, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    if resultado:
        flash('Movimiento registrado exitosamente')
        return redirect(url_for('movimiento.movimiento'))
    else:
        flash('¡Error! ha ocurrido un error al registrar el movimiento')
        return redirect(url_for('movimiento.movimiento'))

# Ruta que registra una entrada en la DB de un producto que no existe     
@movimiento_route.route('/registrar_entrada_no_existente', methods=["POST"])
@login_requerido
@validation_jwt
def registrar_entrada_no_existente(datos_usuario):
    # SEPARAR LOS DOS FORMULARIOS, IDEA: PARA LOS PRODUCTOS QUE NO EXISTEN AUN, DEBERIA PRIMERO CREARLOS Y DESPUES LISTARLOS HACER UN IF QUE VEA SI ESE PRODUCTO EXISTE EN ESA LISTA Y CREAR LA ENTRADA
    tipo_movimiento = 1
    motivo = "Entrada de nuevo producto"
    nombre = request.form['nombre']
    detalles = request.form['detalles']
    imagen = request.files['imagen']
    precio = request.form['precio']
    cantidad = request.form['existencia']
    distribuidor = request.form['distribuidor']
    medida = request.form['medida']
    categoria = request.form['categoria']
    cantidad_minima = request.form['minimo']
    filename = None
    subcarpeta = 'productos'

    if distribuidor == "" or categoria == "" or medida == "":
        flash('¡Error! Complete todos los campos')
        return redirect(url_for('movimiento.movimiento'))

    if not image_verification(imagen):
        flash('Formato de imagen no permitido')
        return redirect(url_for('movimiento.movimiento'))

    print(imagen)

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta, filename))

    archivo = generate_name_unique(filename)
    os.rename(os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta, filename), os.path.join(current_app.config['UPLOAD_FOLDER'], subcarpeta, archivo))
    
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    productos, parametro = productor.create_producto(nombre, detalles, precio, cantidad, date.today(), archivo, distribuidor, categoria, medida, cantidad_minima)
    instancia_conexion.registrar(cursor, productos, parametro)
    consulta, parametros = productor.obtene_por_nombre(nombre, detalles, precio, cantidad, cantidad_minima)
    recuperar_producto = instancia_conexion.uno(cursor, consulta, parametros)
    registrar_movimiento, parametro = historial.movimiento(recuperar_producto[0], cantidad, datetime.now(), session['id_usuario'], motivo, tipo_movimiento)
    instancia_conexion.registrar(cursor, registrar_movimiento, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    
    if resultado:
        flash('Movimiento registrado exitosamente')
        return redirect(url_for('movimiento.movimiento'))
    else:
        flash('¡Error! ha ocurrido un error al registrar el movimiento')
        return redirect(url_for('movimiento.movimiento'))

# Ruta que registra una salida en la DB
@movimiento_route.route('/registrar_salida', methods=["POST"])
@login_requerido
@validation_jwt
def registrar_salida(datos_usuario):
    producto = request.form['producto']
    motivo = "Entrega de producto"
    cantidad = request.form['cantidad_salida']
    tipo_movimiento = 2

    pool_db, cursor = instancia_conexion.iniciar_conexion()
    productos, parametro = productor.obtener_cantidad(producto) 
    cantidad_existencia = instancia_conexion.uno(cursor, productos, parametro) 

    if int(cantidad) <= int(cantidad_existencia[0]) and int(cantidad_existencia[0]) > 0:
        cantidad_total = int(cantidad_existencia[0]) - int(cantidad)
        consulta, parametros = productor.modifica_cantidad(producto, cantidad_total)
        instancia_conexion.registrar(cursor, consulta, parametros)
        consulta, parametros = productor.obtener_uno(producto)
        recuperar_producto = instancia_conexion.uno(cursor, consulta, parametros)
        registrar_movimiento,parametro = historial.movimiento(recuperar_producto[0], cantidad, datetime.now(), session['id_usuario'], motivo, tipo_movimiento)
        instancia_conexion.registrar(cursor, registrar_movimiento, parametro)
        resultado = instancia_conexion.ejecutar_cambio(pool_db)
        instancia_conexion.cerrar_conexion(cursor, pool_db)
        if resultado:
            flash('Movimiento registrado exitosamente')
            return redirect(url_for('movimiento.movimiento'))
        else:
            flash('¡Error! ha ocurrido un error al registrar el movimiento')
            return redirect(url_for('movimiento.movimiento'))
    else:
        flash('El producto elegido no tiene la cantidad en existencia suficiente')
        return redirect(url_for('movimiento.movimiento'))

# Ruta que registra una devolucion en la DB  
@movimiento_route.route("/registrar_devolucion", methods=["POST"])
@login_requerido
@validation_jwt
def registrar_devolucion(datos_usuario):
    producto = request.form['producto']
    motivo = request.form['motivo']
    cantidad = request.form['cantidad_devolucion']
    tipo_movimiento = 3
    tipo_devolucion = request.form['tipo']
    
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    productos, parametro = productor.obtener_cantidad(producto)
    cantidad_existencia = instancia_conexion.uno(cursor, productos, parametro)

    if int(tipo_devolucion) == 1:
        if int(cantidad) <= int(cantidad_existencia[0]) and int(cantidad_existencia[0]) > 0:
            cantidad_total = int(cantidad_existencia[0]) - int(cantidad)
        else:
            instancia_conexion.cerrar_conexion(cursor)
            flash('El producto elegido no tiene la cantidad en existencia suficiente')
            return redirect(url_for('movimiento.movimiento'))
    else:
        cantidad_total = int(cantidad_existencia[0]) + int(cantidad)

    consulta, parametro = productor.modifica_cantidad(producto, cantidad_total)
    instancia_conexion.registrar(cursor, consulta, parametro)
    productos, parametro = productor.obtener_uno(producto)
    recuperar_producto = instancia_conexion.uno(cursor, productos, parametro)
    registrar_movimiento, parametro = historial.movimiento(recuperar_producto[0], cantidad, datetime.now(), session['id_usuario'], motivo, tipo_movimiento)
    instancia_conexion.registrar(cursor, registrar_movimiento, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)

    if resultado:
        flash('Movimiento registrado exitosamente')
        return redirect(url_for('movimiento.movimiento'))
    else:
        flash('¡Error! ha ocurrido un error al registrar el movimiento')
        return redirect(url_for('movimiento.movimiento'))

# Ruta que registra un ajuste en la DB
@movimiento_route.route("/registrar_Ajuste", methods=["POST"])
@login_requerido
@validation_jwt
def registrar_Ajuste(datos_usuario):
    producto = request.form['producto']
    cantidad = request.form['cantidad_ajuste']
    tipo_movimiento = 4
    tipo_devolucion = request.form['tipo']
    
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    productos, parametro = productor.obtener_cantidad(producto)
    cantidad_existencia = instancia_conexion.uno(cursor, productos, parametro)
    
    if int(tipo_devolucion) == 1:
        if int(cantidad) <= int(cantidad_existencia[0]) and int(cantidad_existencia[0]) > 0:
            cantidad_total = int(cantidad_existencia[0]) - int(cantidad)
            motivo = "Error de conteo, disminucion de stock"
        else:
            instancia_conexion.cerrar_conexion()
            flash('El producto elegido no tiene la cantidad en existencia suficiente')
            return redirect(url_for('movimiento.movimiento'))
    else:
        cantidad_total = int(cantidad_existencia[0]) + int(cantidad)
        motivo = "Error de conteo, aumento de stock"

    consulta, parametro = productor.modifica_cantidad(producto, cantidad_total)
    instancia_conexion.registrar(cursor, consulta, parametro)
    productos, parametro = productor.obtener_uno(producto)
    recuperar_producto = instancia_conexion.uno(cursor, productos, parametro)
    registrar_movimiento, parametro = historial.movimiento(recuperar_producto[0], cantidad, datetime.now(), session['id_usuario'], motivo, tipo_movimiento)
    instancia_conexion.registrar(cursor, registrar_movimiento, parametro)
    resultado = instancia_conexion.ejecutar_cambio(pool_db)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
      
    if resultado:
        flash('Movimiento registrado exitosamente')
        return redirect(url_for('movimiento.movimiento'))
    else:
        flash('¡Error! ha ocurrido un error al registrar el movimiento')
        return redirect(url_for('movimiento.movimiento'))