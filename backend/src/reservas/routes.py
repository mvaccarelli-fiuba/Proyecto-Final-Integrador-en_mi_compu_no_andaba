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



         
                                         

                        
