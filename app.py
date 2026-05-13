from flask import Flask
import os
from dotenv import load_dotenv
# import all the routes
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

# main controllator
app=Flask(__name__)
load_dotenv()
configuracion = app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
clave = app.secret_key = os.getenv('SECRET_KEY')

# route login
app.register_blueprint(login_route)

# route dahsboard principal
app.register_blueprint(dashboard_route)

# route productos sin movimientos
app.register_blueprint(sin_movimiento_route)

# route con productos, proveedores y perfiles inactivos
app.register_blueprint(inactivos_route)

# route de materiales de pintura
app.register_blueprint(inventario_route)

# route de proveedores
app.register_blueprint(proveedor_route)

# route de trabajadores
app.register_blueprint(usuario_route)

# route de movimiento 
app.register_blueprint(movimiento_route)

# route de historial de movimientos
app.register_blueprint(historial_route)

# route de stock critico
app.register_blueprint(minimo_route)

# route con la configuraciones
app.register_blueprint(configuracion_route)

# route con el reporte
app.register_blueprint(reporte_route)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

