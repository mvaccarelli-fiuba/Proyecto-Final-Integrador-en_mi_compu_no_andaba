from flask import Blueprint, request, jsonify
import mysql.connector

from src.platos import service
from src.utils import error, require_admin

platos_bp = Blueprint("platos", __name__)


@platos_bp.route("/platos", methods=["GET"])
def get_platos():
    try:
        platos = service.get_platos()
        return jsonify(platos), 200
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener los platos: {err}", 500)


@platos_bp.route("/platos/<int:id>", methods=["GET"])
def get_plato(id):
    try:
        plato = service.get_plato(id)
        return jsonify(plato), 200
    except ValueError as err:
        return error("404", "Not Found", f"Plato no encontrado: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener el plato: {err}", 500)


@platos_bp.route("/platos/<string:restriccion>", methods=["GET"])
def get_platos_con_restriccion(restriccion):
    restriction_types = ["vegano", "vegetariano", "gluten"]
    if restriccion not in restriction_types:
        return error(
            "400",
            "Bad Request",
            "Tipo de restricción debe ser vegano, vegetariano o gluten",
            400,
        )

    try:
        platos = service.get_platos_con_restriccion(restriccion)
        return jsonify(platos), 200
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener los platos con la restricción: {err}", 500)


@platos_bp.route("/platos", methods=["POST"])
@require_admin
def create_plato():
    try:
        plato = service.create_plato(request.json)
        return jsonify({"message": "Plato creado correctamente", "data": plato}), 201
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except ValueError as err:
        return error("400", "Bad Request", f"Error al crear el plato: {err}", 400)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al crear el plato: {err}", 500)


@platos_bp.route("/platos/<int:id>", methods=["PUT"])
@require_admin
def update_plato(id):
    try:
        plato = service.update_plato(id, request.json)
        return jsonify({"message": "Plato actualizado correctamente", "data": plato}), 200
    except ValueError as err:
        return error("404", "Not Found", f"Plato no encontrado: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al actualizar el plato: {err}", 500)


@platos_bp.route("/platos/<int:id>", methods=["DELETE"])
@require_admin
def delete_plato(id):
    try:
        service.delete_plato(id)
        return jsonify({"message": "Plato eliminado correctamente"}), 200
    except ValueError as err:
        return error("404", "Not Found", f"Plato no encontrado: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al eliminar el plato: {err}", 500)


@platos_bp.route("/admin/platos/<int:id>/imagen", methods=["POST"])
@require_admin
def set_plato_imagen(id):
    data = request.get_json()
    if not data:
        return error("400", "Bad Request", "No se enviaron datos", 400)

    url = data.get("url")
    if not url:
        return error("400", "Bad Request", "El campo 'url' es requerido", 400)

    try:
        plato = service.set_plato_imagen_url(id, url)
        return jsonify({"message": "Url de imagen guardada correctamente", "data": plato}), 200
    except ValueError as err:
        message = str(err) or "Plato no encontrado"
        if "no encontrado" in message.lower():
            return error("404", "Not Found", message, 404)
        return error("400", "Bad Request", message, 400)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al guardar la url: {err}", 500)
