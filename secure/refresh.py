from secure.create_jwt import create_jwt
from model_db.conexion import Conexion
from model_db.model_class.model_refresh_token import Refresh_token
from model_db.model_class.model_usuario import Usuario
from secure.create_cookie import create_cookie
from dotenv import load_dotenv
from datetime import date
import uuid

load_dotenv()
refresh = Refresh_token()
user = Usuario()
instancia_conexion = Conexion()

def refresh_login(encode, recovery, recuperado, cursor, pool_db):
    if recovery:
        token = create_cookie(encode, recovery[1])
        return token
    else:
        verify = str(uuid.uuid4())
        query, parameters = refresh.create_refresh(recuperado, verify, False, date.today())
        instancia_conexion.registrar(cursor, query, parameters)
        instancia_conexion.ejecutar_cambio(pool_db)
        token = create_cookie(encode, verify)
        print(cursor)
        return token

def refresh_token_validation(uuid):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    query, parameters = refresh.verify_refresh(uuid, date.today())
    result = instancia_conexion.uno(cursor, query, parameters)
    instancia_conexion.cerrar_conexion(cursor, pool_db)
    return result
    
def refresh_token(result):
    pool_db, cursor = instancia_conexion.iniciar_conexion()
    verify = str(uuid.uuid4())
    try:
        query, parameters = refresh.update_refresh(result[1])
        instancia_conexion.registrar(cursor, query, parameters)
        query, parameters = refresh.create_refresh(result[0], verify, False, date.today())
        instancia_conexion.registrar(cursor, query, parameters)
        instancia_conexion.ejecutar_cambio(pool_db)
        query, parameters = user.obtener_uno_refresh(result[0])
        user_get = instancia_conexion.uno(cursor, query, parameters)
        encode = create_jwt(user_get[0], user_get[1], user_get[2], user_get[3])
        instancia_conexion.cerrar_conexion(cursor, pool_db)
        return encode, verify
    except Exception as e:
        instancia_conexion.cerrar_conexion(cursor, pool_db)
        print(f"Something went wrong: {e}")
        return 'no', 'no'
