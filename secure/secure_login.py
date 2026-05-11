from flask import session, redirect, url_for
def login_requerido(func):
    def wrap(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login.login'))
        return func(*args, **kwargs)
    wrap.__name__ = func.__name__
    return wrap