from flask import Blueprint, flash, redirect, url_for
from middleware.auth import validation_jwt
from datetime import date, datetime
from model_db.class_singlen import productor, historial, usuarios, instancia_conexion
from jinja2 import Environment, FileSystemLoader
from services.generar_reporte import *
# Rutas relacionadas con los reportes
reporte_route = Blueprint('reporte', __name__, template_folder='templates')

# Ruta con la generacion de reportes
@reporte_route.route('/reporte')
@validation_jwt
def reporte_diario(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    # cantidad de hoy en bs
    producto = instancia_conexion.todos(cursor, productor.obtener_cantidad_productos())
    minimo_cantidad = productor.listar_minimo_cantidad()
    # cantidad stock critico
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    texto, parametro = historial.contar_entradas_hoy()
    entradas = instancia_conexion.todos_parametros(cursor, texto, parametro)
    texto, parametro = historial.contar_entradas_total_bs_hoy()
    cantidad_entradas = instancia_conexion.todos_parametros(cursor, texto, parametro)
    texto, parametro = historial.contar_salidas_hoy()
    salidas = instancia_conexion.todos_parametros(cursor, texto, parametro)
    texto, parametro = historial.contar_salidas_total_bs_hoy()
    cantidad_salidas = instancia_conexion.todos_parametros(cursor, texto, parametro)
    texto, parametro = historial.contar_ajustes_hoy()
    ajustes = instancia_conexion.todos_parametros(cursor, texto, parametro)
    texto, parametro = historial.contar_ajustes_total_aumento_hoy()
    cantidad_aumento = instancia_conexion.todos_parametros(cursor, texto, parametro)
    texto, parametro = historial.contar_ajustes_total_disminucion_hoy()
    cantidad_disminucion = instancia_conexion.todos_parametros(cursor, texto, parametro)
    texto, parametro = historial.contar_devoluciones_hoy()
    devoluciones = instancia_conexion.todos_parametros(cursor, texto, parametro)
    texto, parametro = historial.contar_devoluciones_total_bs_hoy()
    cantidad_devoluciones = instancia_conexion.todos_parametros(cursor, texto, parametro)
    fecha = date.today()
    hora = datetime.now()
    hora_exacta = hora.strftime("%H:%M:%S")
    texto, parametro = usuarios.obtener_nombre(datos_usuario['sub'])
    perfiles = instancia_conexion.uno(cursor, texto, parametro)
    print(perfiles)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("/components/formato_reporte_diario.html")  
    plantilla = template.render(valor=producto, cantidad_stock_critico=alerta, entrada_cantidad=entradas, entradas=cantidad_entradas, salida_cantidad=salidas, salidas=cantidad_salidas, ajuste_cantidad=ajustes, ajuste_aumento=cantidad_aumento, ajuste_disminucion=cantidad_disminucion, devoluciones_cantidad=devoluciones, devoluciones_bs=cantidad_devoluciones, fecha=fecha, hora=hora_exacta, perfil=perfiles)
    resultado = generar_reporte_diario(plantilla, fecha)
    if resultado:
        flash("Reporte Creado")
        return redirect(url_for('dashboard.dashboard'))
    else:
        flash("Error, reporte no generado")
        return redirect(url_for('dashboard.dashboard'))

@reporte_route.route('/reporte_mensual')
@validation_jwt
def reporte_mensual(datos_usuario):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    producto = instancia_conexion.todos(cursor, productor.obtener_cantidad_productos())
    minimo_cantidad = productor.listar_minimo_cantidad()
    alerta = instancia_conexion.todos(cursor, minimo_cantidad)
    productos_movimientos = instancia_conexion.todos(cursor, productor.obtener_cantidad_sin_movimientos())
    sin_movimientos_bs = instancia_conexion.todos(cursor, productor.cantidad_sin_movimientos_bs())
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
    fecha = date.today()
    hora = datetime.now()
    mes = fecha.month
    anio = fecha.year
    valor_inicial_inventario = producto[0][0] - total_entradas_bs[0][0] + total_salidas_bs[0][0] - total_ajuste_aumento[0][0] + total_ajuste_disminucion[0][0] - total_devoluciones_bs[0][0]
    valor_promedio = (producto[0][0] + valor_inicial_inventario) / 2
    total = f"{total_salidas_bs[0][0] / valor_promedio:.2f}"
    indice_rotacion = total
    hora_exacta = hora.strftime("%H:%M:%S")
    texto, parametro = usuarios.obtener_nombre(datos_usuario['sub'])
    perfiles = instancia_conexion.uno(cursor, texto, parametro)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("components/formato_reporte_mensual.html")  
    plantilla = template.render(mes=meses[mes-1], anio=anio, saldo_inicial=valor_inicial_inventario, valor_final=producto, critico=alerta, sin_movimiento=productos_movimientos, cantidad_sin_movimiento=sin_movimientos_bs, rotacion_indice=indice_rotacion, cantidad_entradas=total_entradas, entradas=total_entradas_bs,  cantidad_salidas=total_salidas, salidas=total_salidas_bs, cantidad_ajustes=total_ajustes, aumento=total_ajuste_aumento, disminucion=total_ajuste_disminucion, cantidad_devoluciones=total_devoluciones, devolucion=total_devoluciones_bs, fecha_actual=fecha, hora=hora_exacta, perfil=perfiles)
    resultado = generar_reporte_mensual(plantilla, mes)
    if resultado:
        flash("Reporte Creado")
        return redirect(url_for('dashboard.dashboard'))
    else:
        flash("Error, reporte no generado")
        return redirect(url_for('dashboard.dashboard'))