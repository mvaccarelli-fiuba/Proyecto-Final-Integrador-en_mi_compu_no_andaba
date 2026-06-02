from datetime import date, datetime
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
    return value


def convert_row_to_dict(row):
    return {key: convert_value(value) for key, value in row.items()}


def get_all_mesas():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, numero, capacidad, activa
            FROM mesa
            ORDER BY numero
            """)
        rows = cursor.fetchall()
        cursor.close()
        return [convert_row_to_dict(row) for row in rows]
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def get_mesa(id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, numero, capacidad, activa
            FROM mesa
            WHERE id = %s
            """,
            (id,),
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return convert_row_to_dict(row)
        raise ValueError("Mesa no encontrada")
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def create_mesa(mesa_data):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO mesa (numero, capacidad, activa)
            VALUES (%s, %s, %s)
            """,
            (
                mesa_data["numero"],
                mesa_data["capacidad"],
                mesa_data.get("activa", True),
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return get_mesa(new_id)
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def update_mesa(id, mesa_data):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE mesa
            SET numero = %s, capacidad = %s, activa = %s
            WHERE id = %s
            """,
            (
                mesa_data["numero"],
                mesa_data["capacidad"],
                mesa_data.get("activa", True),
                id,
            ),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Mesa no encontrada")
        cursor.close()
        return get_mesa(id)
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def delete_mesa(id):
    """Baja lógica: marca la mesa como inactiva."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE mesa
            SET activa = FALSE
            WHERE id = %s
            """,
            (id,),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Mesa no encontrada")
        cursor.close()
    except mysql.connector.Error:
        raise
    finally:
        conn.close()
