from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from dotenv import load_dotenv
from secure.refresh import *
from secure.create_jwt import *
from secure.refresh import refresh_login
from secure.create_cookie import *
from secure.delete_cookie import delete_cookie
from datetime import date
from model_db.class_singlen import usuarios, refresh, hash, instancia_conexion

load_dotenv()
# Rutas relacionadas al login de la aplicacion web
login_route = Blueprint('login', __name__, template_folder='templates')

# Ruta donde el usuario ingresa los datos y se consulta a la DB
@login_route.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        nombre = request.form['usuario']
        clave = request.form['clave']

        try:
            pool_db, cursor = instancia_conexion.iniciar_conexion()
        except Exception as e:
            print(f"Problem with the service: {e}")
            abort(500)
        texto, parametros = usuarios.login(nombre)
        recuperado = instancia_conexion.uno(cursor, texto, parametros)

        if recuperado:
            rehash = hash.hash_password_verify(recuperado[2], clave, recuperado[0], usuarios, instancia_conexion, cursor, pool_db)
            if rehash == False:
                instancia_conexion.cerrar_conexion(cursor, pool_db)
                flash("¡Error! user or password incorrect.")
                return redirect(url_for('login.login'))
            
            encode = create_jwt(recuperado[0], recuperado[1], recuperado[3], recuperado[4])
            query, parameters = refresh.verify_refresh_login(recuperado[0], date.today())
            recovery = instancia_conexion.uno(cursor, query, parameters)
            token = refresh_login(encode, recovery, recuperado[0], cursor, pool_db)
            instancia_conexion.cerrar_conexion(cursor, pool_db)
            flash(f'¡Bienvenido! {recuperado[1]}')
            
            return token
        else:
            flash("¡Error! The user does not exist")
            return redirect(url_for('login.login'))

    return render_template('login.html')

# Ruta donde se cierra la seccion eliminando los sessions del usuario y volviendo a la vista del Login 
@login_route.route('/close_seccion')
def cerrar_seccion():
    redq = delete_cookie()
    flash('Has cerrado sesion')
    return redq