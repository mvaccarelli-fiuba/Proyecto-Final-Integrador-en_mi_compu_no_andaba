from functools import wraps

from flask import session

from src.utils import error


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_id"):
            return error(
                "401",
                "Unauthorized",
                "Debe iniciar sesión como administrador",
                401,
            )
        return f(*args, **kwargs)

    return decorated
