from flask import abort
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
            self.connection_db = ThreadedConnectionPool(1, 15, dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'))
            pool_db = self.connection_db.getconn()
            cursor = pool_db.cursor()
            return pool_db, cursor
        except Exception as e:
            print("Ha ocurrido un error al conectar a la base de datos: ", e)
            abort(500)
    
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
            return True
        except Exception as e:
            self.revertir_cambio(pool_db)
            print("Ha ocurrido un error al conectar a la base de datos: ", e)
            return False
        
    @classmethod
    def revertir_cambio(self, pool_db):
        pool_db.rollback()

    @classmethod
    def cerrar_conexion(self, cursor, pool_db):
        cursor.close()
        self.connection_db.putconn(pool_db)
        