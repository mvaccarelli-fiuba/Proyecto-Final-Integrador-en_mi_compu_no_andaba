from this import d
from flask import Blueprint, request, jsonify
from src.platos import service
import mysql.connector

platos_bp = Blueprint("platos", __name__)

@platos_bp.route("/platos", methods=["GET"])
def get_platos():
    try:
        platos = service.get_platos()
        return jsonify(platos), 200
    except mysql.connector.Error as err:
        return jsonify({"error": "No se pudo conectar con la base de datos", "detail": str(err)}), 500
    except Exception as err:
        return jsonify({"error": "Ocurrió un error al obtener los platos", "detail": str(err)}), 500


@platos_bp.route("/platos/<int:id>", methods=["GET"])
def get_plato(id):
    try:
        plato = service.get_plato(id)
        return jsonify(plato), 200
    except ValueError as err:
        return jsonify({"error": "Plato no encontrado", "detail": str(err)}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": "No se pudo conectar con la base de datos", "detail": str(err)}), 500
    except Exception as err:
        return jsonify({"error": "Ocurrió un error al obtener el plato", "detail": str(err)}), 500

@platos_bp.route("/platos/<string:restriccion>", methods=["GET"])

def get_platos_con_restriccion(restriccion):
    restriction_types = ["vegano", "vegetariano", "gluten"]
    if restriccion not in restriction_types:
        return jsonify({"error": "Tipo de restricción inválido", "detail": "Tipo de restricción debe ser vegano, vegetariano o gluten"}), 400

    try:
        platos = service.get_platos_con_restriccion(restriccion)
        return jsonify(platos), 200
    except mysql.connector.Error as err:
        return jsonify({"error": "No se pudo conectar con la base de datos", "detail": str(err)}), 500
    except Exception as err:
        return jsonify({"error": "Ocurrió un error al obtener los platos con la restricción", "detail": str(err)}), 500

@platos_bp.route("/platos", methods=["POST"])
def create_plato():
    try:
        plato = service.create_plato(request.json)
        return jsonify({"message": "Plato creado correctamente", "data": plato}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": "No se pudo conectar con la base de datos", "detail": str(err)}), 500
    except ValueError as err:
        return jsonify({"error": "Error al crear el plato", "detail": str(err)}), 400
    except Exception as err:
        return jsonify({"error": "Ocurrió un error al crear el plato", "detail": str(err)}), 500
    
@platos_bp.route("/platos/<int:id>", methods=["PUT"])
def update_plato(id):
    try:
        plato = service.update_plato(id, request.json)
        return jsonify({"message": "Plato actualizado correctamente", "data": plato}), 200
    except ValueError as err:
        return jsonify({"error": "Plato no encontrado", "detail": str(err)}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": "No se pudo conectar con la base de datos", "detail": str(err)}), 500
    except Exception as err:
        return jsonify({"error": "Ocurrió un error al actualizar el plato", "detail": str(err)}), 500


@platos_bp.route("/platos/<int:id>", methods=["DELETE"])
def delete_plato(id):
    try:
        service.delete_plato(id)
        return jsonify({"message": "Plato eliminado correctamente"}), 200
    except ValueError as err:
        return jsonify({"error": "Plato no encontrado", "detail": str(err)}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": "No se pudo conectar con la base de datos", "detail": str(err)}), 500
    except Exception as err:
        return jsonify({"error": "Ocurrió un error al eliminar el plato", "detail": str(err)}), 500