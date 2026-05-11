from flask import Flask
import os
from dotenv import load_dotenv
# Se importan todas las rutas
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

# controlador principal
app=Flask(__name__)
load_dotenv()
configuracion = app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
clave = app.secret_key = os.getenv('SECRET_KEY')

# rutas login
app.register_blueprint(login_route)

# rutas dahsboard principal
app.register_blueprint(dashboard_route)

# rutas productos sin movimientos
app.register_blueprint(sin_movimiento_route)

# rutas con productos, proveedores y perfiles inactivos
app.register_blueprint(inactivos_route)

# Rutas de materiales de pintura
app.register_blueprint(inventario_route)

# Rutas de proveedores
app.register_blueprint(proveedor_route)

# Rutas de trabajadores
app.register_blueprint(usuario_route)

# Rutas de movimiento 
app.register_blueprint(movimiento_route)

# Rutas de historial de movimientos
app.register_blueprint(historial_route)

# Rutas de stock critico
app.register_blueprint(minimo_route)

# Rutas con la configuraciones
app.register_blueprint(configuracion_route)

# Rutas con el reporte
app.register_blueprint(reporte_route)

if __name__ == "__main__":
    app.run(debug=True, port=5001)


"""
request: Permite acceder a los datos que un usuario envía con su petición, como los datos de un formulario o los parámetros de la URL. 
Por ejemplo, si un usuario envía un formulario, request.form contendrá esa información.

redirect: Sirve para redirigir al usuario de una página a otra. Es muy útil después de que un usuario envía un formulario, 
para llevarlo a una página de confirmación.

url_for: Crea una URL para una función específica. En lugar de escribir la ruta (/contacto), usas url_for('contacto'), 
lo que hace tu código más flexible. Si cambias la ruta de la función contacto, no necesitas actualizar el enlace en todo tu código.

render_template: La más importante para crear páginas web. Te permite renderizar archivos HTML que están en una carpeta llamada 
templates. Esto separa la lógica de tu aplicación (en Python) de la estructura de tu página (en HTML).

session: Se utiliza para guardar datos específicos del usuario en el servidor, de forma segura, durante su sesión. Por ejemplo, 
puedes guardar que un usuario ha iniciado sesión.

Atributo,Fuente del dato,Uso principal
request.args,URL (?id=1),"Filtros, búsquedas, navegación."
request.form,Formulario HTML,"Registro de datos, Login, formularios pesados."
request.values,Combinación de ambos,Cuando no te importa de dónde venga el dato.
request.json,Cuerpo en formato JSON,APIs modernas o aplicaciones de JavaScript/React.
request.files,Archivos subidos,Carga de imágenes o documentos.
"""