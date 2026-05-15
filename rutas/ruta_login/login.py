from flask import Blueprint, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv
from model_db.conexion import Conexion
from model_db.model_class.model_usuario import *
from model_db.model_class.model_refresh_token import Refresh_token
from middleware.create_jwt import *
from middleware.auth import data_jwt
from secure.create_cookie import *
from secure.delete_cookie import delete_cookie
from secure.hash_password import Hash_password
from datetime import date
import uuid

load_dotenv()
# Rutas relacionadas al login de la aplicacion web
login_route = Blueprint('login', __name__, template_folder='templates')
usuarios = Usuario()
refresh = Refresh_token()
hash = Hash_password()
instancia_conexion = Conexion()
# Ruta donde el usuario ingresa los datos y se consulta a la DB
@login_route.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        nombre = request.form['usuario']
        clave = request.form['clave']

        pool_db, cursor = instancia_conexion.iniciar_conexion()
        texto, parametros = usuarios.login(nombre)
        recuperado = instancia_conexion.uno(cursor, texto, parametros)

        if recuperado:
            rehash = hash.hash_password_verify(recuperado[2], clave)
            if rehash:
                text, parameters = usuarios.user_rehash(rehash, recuperado[0])
                instancia_conexion.registrar(cursor, text, parameters)
                instancia_conexion.ejecutar_cambio(pool_db)
            elif rehash == False:
                instancia_conexion.cerrar_conexion(cursor, pool_db)
                flash("¡Error! user or password incorrect.")
                return redirect(url_for('login.login'))
            
            encode = create_jwt(recuperado[0], recuperado[1], recuperado[3], recuperado[4])
            query, parameters = refresh.verify_refresh_login(recuperado[0], date.today())
            recovery = instancia_conexion.uno(cursor, query, parameters)

            if recovery:
                token = create_cookie(encode, recovery[1])
            else:
                verify = str(uuid.uuid4())
                query, parameters = refresh.create_refresh(recuperado[0], verify, False, date.today())
                instancia_conexion.registrar(cursor, query, parameters)
                instancia_conexion.ejecutar_cambio(pool_db)
                token = create_cookie(encode, verify)
            instancia_conexion.cerrar_conexion(cursor, pool_db)
            decode = data_jwt(encode)
            flash(f'¡Bienvenido! {decode['usuario_nombre']}')

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