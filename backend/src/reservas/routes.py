from flask import Blueprint, request, jsonify
import mysql.connector

from src.reservas import service
from src.utils import error, require_admin

reservas_bp = Blueprint("reservas", __name__)



@reservas_bp.route("/disponibilidad", methods=["GET"])
def get_disponibilidad():
    cantidad_personas = request.args.get("cantidad_personas")
    fecha = request.args.get("fecha")
    
    if not cantidad_personas or not fecha:
       return error("400","Bad request","El parametro cantidad_personas y fecha son obligatorios",400)

                   
    try:
        mesas = service.get_disponibilidad(int(cantidad_personas), fecha)
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
            "message": "Reserva creada correctamente","data": reserva}), 201
    except ValueError as err:
        return error("404", "Not Found", str(err), 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrió un error al crear la reserva: {err}", 500)


@reservas_bp.route("/reservas/<string:token>", methods=["GET"])
def get_reserva(token):
    try:
        reserva = service.get_reserva(token)

        return jsonify(reserva), 200
    except ValueError as err:
        return error("404", "Not Found", f"Reserva no encontrada: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500) 
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrio un error al obtener la reserva: {err}", 500)


@reservas_bp.route("/reservas/<string:token>/cancelar", methods=["PUT"])
def cancelar_reserva(token):
    try:
        service.cancelar_reserva(token)
        return jsonify({"message": "Reserva cancelada correctamente"}), 200
    except ValueError as err:
        return error("404","Not Found", f"Reserva no encontrada o ya cancelada: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrio un error al cancelar la reserva: {err}", 500)
      

@reservas_bp.route("/admin/reservas/consumir", methods=["POST"])
@require_admin
def consumir_reserva():
    data = request.json()

    if not data or "token" not in data:
        return error("400", "Bad Request", "El token es obligatorio",400)

    try:
        service.consumir_reserva(data["token"])
        return jsonify({"message": "Reserva consumida correctamente"}), 200
    except ValueError as err:
        return error("404", "Not Found", f"Reserva no encontrada o invalida: {err}", 404)
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrio un error al consumir la reserva: {err}", 500) 


@reservas_bp.route("/admin/reservas", methods=["GET"])
@require_admin
def get_reservas():

    estado = request.args.get("estado")
    fecha  = request.args.get("fecha")

    try:
        reservas = service.get_reservas(estado, fecha)

        return jsonify(reservas), 200
    except mysql.connector.Error as err:
        return error("500", "Internal Server Error", f"No se pudo conectar con la base de datos: {err}", 500)    
    except Exception as err:
        return error("500", "Internal Server Error", f"Ocurrio un error al obtener las reservas:{err}", 500)
    

        
   
                                         

                        
