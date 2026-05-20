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


def get_all_resenas():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, reserva_id, nombre, estrellas, comentario, activo, created_at
            FROM resenas
            WHERE activo = TRUE
            ORDER BY created_at DESC
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        return [convert_row_to_dict(row) for row in rows]
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def get_resena(id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, reserva_id, nombre, estrellas, comentario, activo, created_at
            FROM resenas
            WHERE id = %s
            """,
            (id,)
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return convert_row_to_dict(row)
        else:
            raise ValueError
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def create_resena(resena_data):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO resenas (reserva_id, nombre, estrellas, comentario)
            VALUES (%s, %s, %s, %s)
            """,
            (
                resena_data["reserva_id"],
                resena_data["nombre"],
                resena_data["estrellas"],
                resena_data["comentario"]
            )
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return get_resena(new_id)
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def delete_resena(id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE resenas
            SET activo = FALSE
            WHERE id = %s
            """,
            (id,)
        )
        conn.commit()
        cursor.close()
    except mysql.connector.Error:
        raise
    finally:
        conn.close()