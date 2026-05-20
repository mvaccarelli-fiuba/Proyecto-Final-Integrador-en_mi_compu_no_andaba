from functools import wraps
from flask import jsonify, session


def error(codigo, mensaje, descripcion, codigo_estatus):
    """
    Devuelve una respuesta de error con formato consistente para toda la API.

    """
    return (
        jsonify(
            {
                "errors": [
                    {
                        "code": codigo,
                        "message": mensaje,
                        "level": "error",
                        "description": descripcion,
                    }
                ]
            }
        ),
        codigo_estatus,
    )


def require_admin(f):
    """
    Decorador para proteger endpoints que requieren admin logueado.
    Si no hay sesión activa, devuelve 401 sin ejecutar el endpoint.
    """

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
