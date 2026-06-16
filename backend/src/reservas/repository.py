from datetime import date, datetime, timedelta
from decimal import Decimal
import mysql.connector

from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def convert_value(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, timedelta):
        # MySQL devuelve TIME como timedelta. Convertimos a "HH:MM:SS".
        total_seconds = int(value.total_seconds())
        horas = total_seconds // 3600
        minutos = (total_seconds % 3600) // 60
        segundos = total_seconds % 60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    return value


def convert_row_to_dict(row):
    return {key: convert_value(value) for key, value in row.items()}


def get_disponibilidad(cantidad_personas, fecha):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT *
            FROM mesa 
            WHERE capacidad >= %s
            AND activa = True
            AND id NOT IN (
                SELECT mesa_id
                FROM reserva
                WHERE fecha = %s
                AND estado = "confirmada"
            )
            """,
            (cantidad_personas, fecha),
        )

        rows = cursor.fetchall()
        cursor.close()
        return [convert_row_to_dict(row) for row in rows]
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def create_reserva(reserva_data):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id
            FROM mesa
            WHERE capacidad >= %s
            AND activa = TRUE
            ORDER BY capacidad ASC
            LIMIT 1
            """,
            (reserva_data["cantidad_personas"],),
        )
        mesa = cursor.fetchone()
        if not mesa:
            raise ValueError("No hay mesas disponibles")
        cursor.execute(
            """
            INSERT INTO reserva
            (
                token,
                cliente_nombre,
                cliente_email,
                cantidad_personas,
                fecha,
                hora_inicio,
                mesa_id
            )   
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                reserva_data["token"],
                reserva_data["cliente_nombre"],
                reserva_data["cliente_email"],
                reserva_data["cantidad_personas"],
                reserva_data["fecha"],
                reserva_data["hora_inicio"],
                mesa["id"],
            ),
        )
        conn.commit()
        nueva_reserva_id = cursor.lastrowid
        cursor.close()
        return nueva_reserva_id
    except mysql.connector.Error as err:
        if err.errno == 1062:
            raise ValueError

        raise
    finally:
        if conn.is_connected():
            conn.close()


def get_reserva(token):
    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM reserva 
            WHERE token = %s
            """,
            (token,),
        )

        reserva = cursor.fetchone()
        cursor.close()

        if not reserva:
            raise ValueError("Reserva no encontrada")

        return convert_row_to_dict(reserva)

    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def cancelar_reserva(token):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE reserva
            SET estado = "cancelada",
            cancelado_en = NOW()
            WHERE token = %s
            AND estado = "confirmada"
            """,
            (token,),
        )

        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Reserva no encontrada o ya cancelada")

        cursor.close()
        return True

    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def consumir_reserva(token):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
           UPDATE reserva
           SET estado = "consumida", 
           consumido_en = NOW()
           WHERE token = %s
           AND estado = "confirmada"
           """,
            (token,),
        )

        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Reserva no encontrada o invalida")

        cursor.close()
        return True

    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def get_reservas(estado=None, fecha=None):
    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        if estado is None and fecha is None:
            cursor.execute("""
                SELECT *
                FROM reserva
                """)
        else:
            cursor.execute(
                """
                SELECT * 
                FROM reserva
                WHERE (%s is null or estado = %s)
                AND (%s is null or fecha = %s)
                """,
                (estado, estado, fecha, fecha),
            )

        reservas = cursor.fetchall()

        for reserva in reservas:
            if reserva["estado"] == "confirmada" and reserva["fecha"] < date.today():
                reserva["estado"] = "expirada"

        cursor.close()

        return [convert_row_to_dict(row) for row in reservas]

    except mysql.connector.Error:
        raise

    finally:
        if conn.is_connected():
            conn.close()


def get_reserva_por_token(token):
    """Devuelve la reserva si existe, o None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, token, cliente_nombre, cliente_email, estado
            FROM reserva
            WHERE token = %s
            """,
            (token,),
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return convert_row_to_dict(row)
        return None
    finally:
        if conn.is_connected():
            conn.close()


def existe_resena_para_reserva(reserva_id):
    """Devuelve True si ya existe una reseña para esa reserva."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM resena WHERE reserva_id = %s",
            (reserva_id,),
        )
        existe = cursor.fetchone() is not None
        cursor.close()
        return existe
    finally:
        if conn.is_connected():
            conn.close()
