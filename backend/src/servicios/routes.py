from flask import Blueprint, jsonify, request
import mysql.connector

from src.servicios import service
from src.utils import error

servicios_bp = Blueprint("servicios", __name__)

#OBTENER SERVICIOS

@servicios_bp.route("/servicios", methods=["GET"])
def get_servicios():
    try:
        servicios = service.get_servicios()
        return jsonify(servicios), 200
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener los servicios: {err}", 500)

#CREAR SERVICIO

@servicios_bp.route("/servicios", methods=['POST'])
def crear_servicio():
    data = request.get_json()
    if not data or not data.get("nombre"):
        return error("400", "Bad Request", "El campo nombre es requerido", 400)
    try:
        servicio = service.create_servicio(data)
        return jsonify({"message": "Servicio creado correctamente", "data": servicio}), 201
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al crear el servicio: {err}", 500)
