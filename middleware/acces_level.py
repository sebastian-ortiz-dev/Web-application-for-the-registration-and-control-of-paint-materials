from flask import request, abort
from middleware.decode import data_jwt

def validation_acces(func):
    def wrap(*args, **kwargs):
        data = data_jwt(request.cookies.get('token'))
        if data['nivel_acceso'] != "Administrador":
            abort(403)
        return func(*args, **kwargs)
    wrap.__name__ = func.__name__
    return wrap