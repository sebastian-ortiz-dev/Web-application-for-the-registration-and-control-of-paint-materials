from flask import redirect, url_for, request, flash
from middleware.refresh import refresh_token_validation, refresh_token
from secure.create_cookie import create_cookie_refresh
from dotenv import load_dotenv
import jwt
import os

load_dotenv()
def data_jwt(encode):
    decode = jwt.decode(encode, key=os.getenv("KEY"), algorithms="HS256")
    return decode

def validation_jwt(func):
    def wrap(*args, **kwargs):
        try:
            dato = jwt.decode(request.cookies.get("token"), key=os.getenv("KEY"), algorithms="HS256") 
        except jwt.ExpiredSignatureError as e:
            result = refresh_token_validation(request.cookies.get("refresh"))
            if result:
                encode, uuid_get = refresh_token(result)
                if encode == 'no' and uuid_get == 'no':
                    print(f"Token expirate: {e}")
                    flash("Sesion expirate")
                    return redirect(url_for('login.login'))
                resq = create_cookie_refresh(request.full_path, encode, uuid_get)
                return resq
            else:
                print(f"Token expirate: {e}")
                flash("Sesion expirate")
                return redirect(url_for('login.login'))
        except jwt.InvalidTokenError as e:
            print(f"Token invalidate: {e}")
            flash("Sesion invalidate")
            return redirect(url_for('login.login'))
        return func(dato, *args, **kwargs)
    wrap.__name__ = func.__name__
    return wrap