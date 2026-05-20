from flask import Blueprint, request, jsonify
from flask import request, session
import mysql.connector
from src.resenas import service
from src.utils import error, require_admin



resenas_bp = Blueprint("resenas", __name__)


@resenas_bp.route("/resenas", methods=["GET"])
def get_resenas():
    try:
        resenas = service.get_resenas()
        return jsonify(resenas), 200
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener las reseñas: {err}", 500)


@resenas_bp.route("/resenas/<int:id>", methods=["GET"])
def get_resena(id):
    try:
        resena = service.get_resena(id)
        return jsonify(resena), 200
    except ValueError as err:
        return error("404", "Not Found", f"Reseña no encontrada: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener la reseña: {err}", 500)


@resenas_bp.route("/resenas", methods=["POST"])
def create_resena():
    try:
        resena = service.create_resena(request.json)
        return jsonify({"message": "Reseña creada correctamente", "data": resena}), 201
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except ValueError as err:
        return error("400", "Bad Request", f"Error al crear la reseña: {err}", 400)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al crear la reseña: {err}", 500)


@resenas_bp.route("/admin/resenas/<int:id>", methods=["DELETE"])
@require_admin
def delete_resena(id):
    try:
        service.delete_resena(id)
        return jsonify({"message": "Reseña eliminada correctamente"}), 200
    except ValueError as err:
        return error("404", "Not Found", f"Reseña no encontrada: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al eliminar la reseña: {err}", 500)