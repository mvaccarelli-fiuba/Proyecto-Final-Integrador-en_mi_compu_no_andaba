from flask import Blueprint, request, jsonify
import mysql.connector

from src.mesas import service
from src.utils import error, require_admin

mesas_bp = Blueprint("mesas", __name__)


@mesas_bp.route("/mesas", methods=["GET"])
@require_admin
def get_mesas():
    try:
        mesas = service.get_all_mesas()
        if not mesas:
            return "", 204
        return jsonify(mesas), 200
    except mysql.connector.Error:
        return error("500", "Internal Server Error", "Error al consultar la DB", 500)


@mesas_bp.route("/mesas/<int:id>", methods=["GET"])
@require_admin
def get_mesa(id):
    try:
        mesa = service.get_mesa(id)
        return jsonify(mesa), 200
    except ValueError:
        return error("404", "Not Found", f"Mesa {id} no encontrada", 404)
    except mysql.connector.Error:
        return error("500", "Internal Server Error", "Error al consultar la DB", 500)


@mesas_bp.route("/mesas", methods=["POST"])
@require_admin
def crear_mesa():
    try:
        data = request.get_json()
        if not data:
            return error("400", "Bad Request", "No se enviaron datos", 400)

        mesa = service.create_mesa(data)
        return jsonify(mesa), 201
    except ValueError as e:
        return error("400", "Bad Request", str(e), 400)
    except mysql.connector.IntegrityError:
        return error("409", "Conflict", "Ya existe una mesa con ese número", 409)
    except mysql.connector.Error:
        return error("500", "Internal Server Error", "Error al consultar la DB", 500)


@mesas_bp.route("/mesas/<int:id>", methods=["PUT"])
@require_admin
def editar_mesa(id):
    try:
        data = request.get_json()
        if not data:
            return error("400", "Bad Request", "No se enviaron datos", 400)

        mesa = service.update_mesa(id, data)
        return jsonify(mesa), 200
    except ValueError as e:
        msg = str(e)
        if "no encontrada" in msg:
            return error("404", "Not Found", msg, 404)
        return error("400", "Bad Request", msg, 400)
    except mysql.connector.IntegrityError:
        return error("409", "Conflict", "Ya existe una mesa con ese número", 409)
    except mysql.connector.Error:
        return error("500", "Internal Server Error", "Error al consultar la DB", 500)


@mesas_bp.route("/mesas/<int:id>", methods=["DELETE"])
@require_admin
def eliminar_mesa(id):
    try:
        service.delete_mesa(id)
        return "", 204
    except ValueError:
        return error("404", "Not Found", f"Mesa {id} no encontrada", 404)
    except mysql.connector.Error:
        return error("500", "Internal Server Error", "Error al consultar la DB", 500)
