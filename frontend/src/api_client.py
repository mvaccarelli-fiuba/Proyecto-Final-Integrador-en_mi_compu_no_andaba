"""
Todas las rutas del frontend usan estas funciones en vez de hacer
requests sueltos. Si cambia la URL del backend, se toca acá.
"""

import os
import requests
from flask import session

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")
TIMEOUT = 5  # segundos


def get(path, **kwargs):
    """GET al backend. Si el backend está caído, devuelve None."""
    return _request("GET", path, **kwargs)


def post(path, json=None, **kwargs):
    return _request("POST", path, json=json, **kwargs)


def put(path, json=None, **kwargs):
    return _request("PUT", path, json=json, **kwargs)


def delete(path, **kwargs):
    return _request("DELETE", path, **kwargs)


def _request(method, path, **kwargs):
    """
    Hace el request al backend. Devuelve la respuesta de requests
    o None si hubo un problema de conexión.
    """
    url = f"{BACKEND_URL}{path}"

    # Reenvía la cookie de sesión del backend si la tenemos guardada.
    # Esto es lo que mantiene al admin "logueado" en el backend
    # cuando el frontend hace requests a /admin/* o protegidos.
    cookies = {}
    backend_cookie = session.get("backend_session_cookie")
    if backend_cookie:
        cookies["session"] = backend_cookie

    try:
        response = requests.request(
            method,
            url,
            cookies=cookies,
            timeout=TIMEOUT,
            **kwargs,
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] No se pudo conectar al backend: {e}")
        return None


def extract_session_cookie(response):
    """
    Después de un POST /auth/login al backend, extrae la cookie
    de sesión para que el frontend la guarde y la reenvíe en
    requests posteriores.

    El backend devuelve la cookie en el header 'Set-Cookie'.
    """
    if response is None:
        return None
    return response.cookies.get("session")
