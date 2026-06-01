from functools import wraps
from flask import session, redirect, url_for


def require_admin(f):
    """
    Decorador para proteger rutas del frontend que requieren admin.
    Si no hay sesión, redirige a /login.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper
