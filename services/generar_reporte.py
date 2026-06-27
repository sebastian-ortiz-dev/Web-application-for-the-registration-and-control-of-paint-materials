import os
import platform
from flask import current_app

if platform.system() == "Windows":
    os.add_dll_directory(r"C:\Users\sebas\Desktop\GTK3-Runtime_Win64\bin")
else:
    ruta_libre = '/lib/x86_64-linux-gnu'
    os.environ['LD_LIBRARY_PATH'] = f'{ruta_libre}:{os.environ.get('LD_LIBRARY_PATH', ' ')}'
ruta = os.path.join('Downloads')

from weasyprint import HTML
 
meses = [
    "Enero", "Febrero", "Marzo", "Abril", 
    "Mayo", "Junio", "Julio", "Agosto", 
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

def generar_reporte_diario(vista, fecha):
    try:
        fecha = fecha
        if current_app.config['TESTING'] == True:
            nombre = f"./reportes_test/reporte_diario_{fecha}.pdf"
        else:
            nombre = f"./reportes/reporte_diario_{fecha}.pdf"
        ruta_final = os.path.expanduser(nombre)
        HTML(string=vista).write_pdf(ruta_final)
        return True
    except Exception as e:
        print(f"Error reporte no generado: {e}")
        return False
    
def generar_reporte_mensual(vista, mes):
    try:
        mes = meses[mes - 1]
        if current_app.config['TESTING'] == True:
            nombre = f"./reportes_test/reporte_mensual_{mes}.pdf"
        else:
            nombre = f"./reportes/reporte_mensual_{mes}.pdf"
        ruta_final = os.path.expanduser(nombre)
        HTML(string=vista).write_pdf(ruta_final)
        return True
    except Exception as e:
        print(f"Error reporte no generado: {e}")
        return False