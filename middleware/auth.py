from flask import redirect, url_for, request, flash
from middleware.refresh import refresh_token_validation, refresh_token
from middleware.decode import data_jwt
from secure.create_cookie import create_cookie_refresh
import jwt


def validation_jwt(func):
    def wrap(*args, **kwargs):
        try:
            dato = data_jwt(request.cookies.get('token'))
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