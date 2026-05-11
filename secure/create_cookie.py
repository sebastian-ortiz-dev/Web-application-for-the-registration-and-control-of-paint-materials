from flask import redirect, url_for
import uuid

def create_cookie(encode, uuid_get):
    cookie = redirect(url_for('dashboard.dashboard'))
    cookie.set_cookie('token', value=encode, path='/', httponly=True, secure=False, samesite="Lax")
    cookie.set_cookie('refresh', value=uuid_get, path='/', httponly=True, secure=False, samesite='Lax')
    return cookie

def create_cookie_refresh(url, encode, uuid_new):
    cookie = redirect(url)
    cookie.set_cookie('token', value=encode, path='/', httponly=True, secure=False, samesite="Lax")
    cookie.set_cookie('refresh', value=uuid_new, path='/', httponly=True, secure=False, samesite='Lax')
    return cookie