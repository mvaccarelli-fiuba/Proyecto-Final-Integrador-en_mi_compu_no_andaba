from flask import Blueprint, request, jsonify
import mysql.connector
from src.stats import service
from src.stats import repository
from src.utils import error, require_admin

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/admin/stats/reservas", methods=["GET"])
@require_admin
def stats_reservas():
    periodo = request.args.get("periodo", "meses").lower()

    try:
        data = service.get_stats_reservas(periodo)
        return jsonify({"periodo": periodo, "data": data}), 200
    except mysql.connector.Error as err:
        return error(
            "500",
            "Internal Server Error",
            f"No se pudo conectar con la base de datos: {err}",
            500,
        )
    except Exception as err:
        return error(
            "500",
            "Internal Server Error",
            f"Ocurrió un error al obtener las estadísticas: {err}",
            500,
        )


@stats_bp.route("/admin/stats/cancelaciones", methods=["GET"])
@require_admin
def stats_cancelaciones():
    try:
        data = service.get_stats_cancelaciones()
        return jsonify({"data": data}), 200
    except mysql.connector.Error as err:
        return error(
            "500",
            "Internal Server Error",
            f"No se pudo conectar con la base de datos: {err}",
            500,
        )
    except Exception as err:
        return error(
            "500",
            "Internal Server Error",
            f"Ocurrió un error al obtener las estadísticas: {err}",
            500,
        )


@stats_bp.route("/admin/stats/ocupacion", methods=["GET"])
@require_admin
def stats_ocupacion():
    try:
        data = service.get_stats_ocupacion()
        return jsonify(data), 200
    except mysql.connector.Error as err:
        return error(
            "500",
            "Internal Server Error",
            f"No se pudo conectar con la base de datos: {err}",
            500,
        )
    except Exception as err:
        return error(
            "500",
            "Internal Server Error",
            f"Ocurrió un error al obtener las estadísticas: {err}",
            500,
        )
