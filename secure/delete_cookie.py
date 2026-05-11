from flask import redirect, url_for, request

def delete_cookie():
    cookie = redirect(url_for('login.login'))
    print(request.cookies.get("token"), request.cookies.get("refresh"))
    cookie.set_cookie('token', value=" ", path='/', httponly=True, secure=False, samesite="Lax", max_age=0)
    cookie.set_cookie('refresh', value=" ", path='/', httponly=True, secure=False, samesite="Lax", max_age=0)
    return cookie