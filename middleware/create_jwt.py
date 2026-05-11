from dotenv import load_dotenv
import jwt
import time
import math
import os

load_dotenv()

def create_jwt(sub, name, image, level_acces):
    iat = math.floor(time.time())
    exp = iat + (15 * 60)
    encode = jwt.encode({ "iss": "pintuplomer", "sub": f"{sub}", "usuario_nombre": name, "imagen_usuario": image, "nivel_acceso": level_acces, "iat": iat, "exp": exp }, key=os.getenv("KEY"), algorithm="HS256")
    return encode