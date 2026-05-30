from datetime import date, datetime
from decimal import Decimal
import mysql.connector

from config import DB_CONFIG

RESTRICCION_COLUMNS = {
    "vegano": "es_vegano",
    "vegetariano": "es_vegetariano",
    "gluten": "sin_gluten",
}

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


def get_all_platos():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"""
            SELECT id, nombre, descripcion, precio,
                es_vegano AS vegano,
                es_vegetariano AS vegetariano,
                sin_gluten AS gluten,
                imagen_url,
                disponible AS activo,
                created_at,
                categoria_id
            FROM plato
            WHERE disponible = TRUE
            ORDER BY id
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


def get_plato(id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"""
            SELECT id, nombre, descripcion, precio,
                es_vegano AS vegano,
                es_vegetariano AS vegetariano,
                sin_gluten AS gluten,
                imagen_url,
                disponible AS activo,
                created_at,
                categoria_id
            FROM plato
            WHERE id = %s
            """,
            (id,),
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return convert_row_to_dict(row)
        raise ValueError
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def get_platos_con_restriccion(restriccion):
    column = RESTRICCION_COLUMNS.get(restriccion)
    if column is None:
        raise ValueError(f"Restricción no válida: {restriccion}")

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            f"""
            SELECT id, nombre, descripcion, precio,
                es_vegano AS vegano,
                es_vegetariano AS vegetariano,
                sin_gluten AS gluten,
                imagen_url,
                disponible AS activo,
                created_at,
                categoria_id
            FROM plato
            WHERE {column} = TRUE AND disponible = TRUE
            ORDER BY id
            LIMIT 10
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        return [convert_row_to_dict(row) for row in rows]
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def create_plato(plato_data):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO plato (
                nombre, descripcion, precio, categoria_id,
                es_vegano, es_vegetariano, sin_gluten, imagen_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                plato_data["nombre"],
                plato_data.get("descripcion", ""),
                plato_data["precio"],
                plato_data.get("categoria_id", 1),
                plato_data.get("vegano", False),
                plato_data.get("vegetariano", False),
                plato_data.get("gluten", False),
                plato_data.get("imagen_url", ""),
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return get_plato(new_id)
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def update_plato(id, plato_data):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE plato
            SET nombre = %s, descripcion = %s, precio = %s,
                es_vegano = %s, es_vegetariano = %s, sin_gluten = %s,
                imagen_url = %s, categoria_id = %s
            WHERE id = %s
            """,
            (
                plato_data["nombre"],
                plato_data.get("descripcion", ""),
                plato_data["precio"],
                plato_data.get("vegano", False),
                plato_data.get("vegetariano", False),
                plato_data.get("gluten", False),
                plato_data.get("imagen_url", ""),
                plato_data.get("categoria_id", 1),
                id,
            ),
        )
        conn.commit()
        cursor.close()
        return get_plato(id)
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def update_plato_imagen_url(id, imagen_url):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE plato
            SET imagen_url = %s
            WHERE id = %s
            """,
            (imagen_url, id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Plato no encontrado")
        cursor.close()
        return get_plato(id)
    except mysql.connector.Error:
        raise
    finally:
        conn.close()


def delete_plato(id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE plato
            SET disponible = FALSE
            WHERE id = %s
            """,
            (id,),
        )
        conn.commit()
        cursor.close()
    except mysql.connector.Error:
        raise
    finally:
        conn.close()
