from flask import Blueprint, request, jsonify
import mysql.connector

from src.reservas import service
from src.utils import error, require admin
reservas_bp = Blueprint("reservas", __name__)


@reservas_bp.route("/disponibilidad", methods=["GET"]
def get_disponibilidad():
    cantidad_personas = request.args.get("cantidad_personas")

    if not cantidad_personas:
       return error("400","Bad request","El parametro cantidad_personas es obligatorio",400)

                   
   try:
       mesas = service.get_disponibilidad(int(cantidad_personas))
       return jsonify(mesas), 200

   except mysql.connector.Error as err:
       return error("500","Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)

   
   except Exception as err:
      return error("500","Internal Server Error", f"Ocurrio un error al obtener la disponibilidad: {err}", 500)


@reservas_bp.route("/reservas", methods=["POST"])
def create_reserva():
    reserva_data = request.json

    if not reserva_data:
        return error("400","Bad Request","No se enviaron datos",400)

    campos_obligatorios = [ 
        "cliente_nombre",
        "cliente_email",
        "cantidad_personas",
        "fecha",
        "hora_inicio"
      ]
    for campo in campos_obligatorios:
        if campo not in reserva_data:
            return error("400","Bad Request",f"El campo {campo} es obligatorio", 400)

    try:
        reserva = service.create_reserva(reserva_data)

        return jsonify({
            "message": "Reserva creada correctamente","data": reserva}), 201)
    except ValueError as err:
        return error("404", "Not Found", str(err), 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al crear la reserva: {err}", 500)
   
                                         

                        
