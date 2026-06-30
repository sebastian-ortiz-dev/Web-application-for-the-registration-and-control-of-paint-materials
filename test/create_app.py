from flask import Flask, abort, request
from rutas.ruta_login.login import login_route
from rutas.ruta_inventario.inventario import inventario_route
from rutas.ruta_proveedor.proveedores import proveedor_route
from rutas.ruta_usuario.usuarios import usuario_route
from rutas.ruta_movimientos.movimientos import movimiento_route
from rutas.ruta_historial.historial_movimientos import historial_route
from rutas.ruta_minimo.minimo import minimo_route
from rutas.ruta_dashboard.dashboard import dashboard_route
from rutas.ruta_sin_movimiento.sin_movimiento import sin_movimiento_route
from rutas.ruta_inactivos.inactivos import inactivos_route
from rutas.ruta_configuraciones.configuraciones import configuracion_route
from rutas.ruta_reporte.reportes import reporte_route
from rutas.ruta_error_handler.error_handler import handler_error_route
from secure.create_cookie import create_cookie_refresh
import os
import jwt
import time
import math
import uuid

base_dir = os.path.dirname(os.path.abspath(__file__))
template_route = os.path.join(base_dir, "..", "templates")

def crear_app(config_name="development"):
    app=Flask(__name__, template_folder=template_route)

    if config_name == "testing":
        app.config.update({"TESTING": True})

    @app.route("/error-forzado")
    def error():
        abort(500)

    @app.route("/login-jwt")
    def jwt_expirete():
        credentials = ["admin", "usuario_defecto.png", "Admin"]
        encode = jwt.encode({ "iss": "pintuplomer", "sub": f"{1}", "usuario_nombre": credentials[0], "imagen_usuario": credentials[1], "nivel_acceso": credentials[2], "iat": math.floor(time.time()), "exp": math.floor(time.time()) }, key=os.getenv("KEY"), algorithm="HS256")
        return create_cookie_refresh("/principal", encode, str(uuid.uuid4()))

    @app.route("/refreh")
    def get_refresh():
        return request.cookies.get("refresh")

    app.register_blueprint(login_route)
    app.register_blueprint(handler_error_route)
    app.register_blueprint(dashboard_route)
    app.register_blueprint(sin_movimiento_route)
    app.register_blueprint(inactivos_route)
    app.register_blueprint(inventario_route)
    app.register_blueprint(proveedor_route)
    app.register_blueprint(usuario_route)
    app.register_blueprint(movimiento_route)
    app.register_blueprint(historial_route)
    app.register_blueprint(minimo_route)
    app.register_blueprint(configuracion_route)
    app.register_blueprint(reporte_route)

    return app
    
