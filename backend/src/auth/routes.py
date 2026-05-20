from flask import Blueprint, request, jsonify, session
from src.auth import service
from src.utils import error

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return error("400", "Bad Request", "No se enviaron datos", 400)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error("400", "Bad Request", "email y password son requeridos", 400)

    admin = service.login(email, password)

    if admin is None:
        return error("401", "Unauthorized", "Credenciales inválidas", 401)

    session["admin_id"] = admin["id"]

    return jsonify({"admin": admin}), 200
