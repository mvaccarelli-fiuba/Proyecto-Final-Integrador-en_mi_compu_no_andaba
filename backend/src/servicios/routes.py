from flask import Blueprint, jsonify
import mysql.connector

from src.servicios import service
from src.utils import error

servicios_bp = Blueprint("servicios", __name__)


@servicios_bp.route("/servicios", methods=["GET"])
def get_servicios():
    try:
        servicios = service.get_servicios()
        return jsonify(servicios), 200
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al obtener los servicios: {err}", 500)
