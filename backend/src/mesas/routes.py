from flask import Blueprint, request, jsonify
from src.mesas import service
from src.utils import error
import mysql.connector

mesas_bp = Blueprint("mesas", __name__)

@mesas_bp.route("/admin/mesas", methods=["GET"])
def get_mesas():
    try:
        mesa = service.get_mesas()
        return jsonify(mesa), 200
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener las mesas: {err}", 500)

@mesas_bp.route("/admin/mesas/<int:id>", methods=["GET"])
def get_mesa(id):
    try:
        mesa = service.get_mesa(id)
        return jsonify({"message": "Mesa encontrada", "data": mesa}), 200
    except ValueError as err:
        return error("404", "Not Found", f"Mesa no encontradada: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener la mesa: {err}", 500)

@mesas_bp.route("/admin/mesas", methods=["POST"])
def create_mesa():
    try:
        mesa = service.create_mesa(request.json)
        return jsonify({"message": "Mesa creada correctamente", "data": mesa}), 200
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al crear la mesa: {err}", 500)

@mesas_bp.route("/admin/mesas/<int:id>", methods=["PUT"])
def update_mesa(id):
    try:
        mesa = service.update_mesa(id, request.json)
        return jsonify({"message": "Mesa actualizada correctamente", "data": mesa}), 200

    except ValueError as err:
        return error("404", "Not Found", f"Mesa no encontradada: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al actualizar la mesa: {err}", 500)

@mesas_bp.route("/admin/mesas/<int:id>", methods=["DELETE"])
def delete_mesa(id):
    try:
        mesa = service.delete_mesa(id)
        return jsonify({"message": "Mesa eliminada correctamente"}), 200
    except ValueError as err:
        return error("404", "Not Found", f"Mesa no encontradada: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al eliminar la mesa: {err}", 500)
