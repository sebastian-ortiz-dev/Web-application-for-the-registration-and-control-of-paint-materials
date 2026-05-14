from flask import redirect, url_for, flash, session, request
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
import os
from dotenv import load_dotenv

load_dotenv()

class Conexion():
    def __init__(self):
        pass
        
    @classmethod
    def iniciar_conexion(self):
        try:
            # self.db = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'))
            self.connection_db = ThreadedConnectionPool(1, 15, dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port='5432')
            pool_db = self.connection_db.getconn()
            cursor = pool_db.cursor()
            # cursor = self.db.cursor()
            return pool_db, cursor
        except Exception as e:
            print("Ha ocurrido un error al conectar a la base de datos: ", e)
            flash("¡Error! Ha ocurrido un error en el servidor intentelo otra vez mas tarde")
            return redirect(request.path)
    
    def todos(self, ejecuta, texto):
        ejecuta.execute(texto)
        return ejecuta.fetchall()
    
    def todos_parametros(self, ejecuta, texto, parametros):
        ejecuta.execute(texto, parametros)
        return ejecuta.fetchall()

    def uno(self, ejecuta, texto, parametros):
        ejecuta.execute(texto, parametros)
        return ejecuta.fetchone()        

    def registrar(self, ejecuta, texto, parametros):
        ejecuta.execute(texto, parametros)
            
    @classmethod
    def ejecutar_cambio(self, pool_db):
        try:
            pool_db.commit()
            #self.db.commit()
            return True
        except Exception as e:
            pool_db.rollback()
            # self.db.rollback()
            print("Ha ocurrido un error al conectar a la base de datos: ", e)
            flash("¡Error! Ha ocurrido un error al realizar los cambios, intentelo mas tarde")

    @classmethod
    def cerrar_conexion(self, cursor, pool_db):
        cursor.close()
        self.connection_db.putconn(pool_db)
        #self.db.close()
        

"""def registrar(self, ejecuta, texto, parametros):
        try:
            ejecuta.execute(texto, parametros)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print("Ha ocurrido un error al conectar a la base de datos: ", e)
            flash("¡Error! Ha ocurrido un error al realizar los cambios")
            if session['nivel_acceso'] == 'Administrador':
                return redirect(url_for('inventario.index'))
            else:
                return redirect(url_for('inventario.trabajador'))"""