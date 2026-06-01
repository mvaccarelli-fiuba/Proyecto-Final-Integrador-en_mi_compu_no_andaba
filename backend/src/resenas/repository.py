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
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, reserva_id,
                autor AS nombre,
                puntaje AS estrellas,
                comentario,
                publicada AS activo,
                creado_en AS created_at
            FROM resena
            WHERE publicada = TRUE
            ORDER BY creado_en DESC
            """)
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
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, reserva_id,
                autor AS nombre,
                puntaje AS estrellas,
                comentario,
                publicada AS activo,
                creado_en AS created_at
            FROM resena
            WHERE id = %s
            """,
            (id,),
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return convert_row_to_dict(row)
        raise ValueError("Reseña no encontrada")
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
            INSERT INTO resena (reserva_id, autor, puntaje, comentario)
            VALUES (%s, %s, %s, %s)
            """,
            (
                resena_data["reserva_id"],
                resena_data["nombre"],
                resena_data["estrellas"],
                resena_data["comentario"],
            ),
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
            UPDATE resena
            SET publicada = FALSE
            WHERE id = %s
            """,
            (id,),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Reseña no encontrada")
        cursor.close()
    except mysql.connector.Error:
        raise
    finally:
        conn.close()
