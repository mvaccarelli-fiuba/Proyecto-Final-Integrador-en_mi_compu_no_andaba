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

def get_all_platos():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nombre, descripcion, precio, vegano, vegetariano, gluten, imagen_url, activo, created_at
            FROM platos
            WHERE activo = TRUE
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
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nombre, descripcion, precio, vegano, vegetariano, gluten, imagen_url, activo, created_at
            FROM platos
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

def get_platos_con_restriccion(restriccion):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nombre, descripcion, precio, vegano, vegetariano, gluten, imagen_url, activo, created_at
            FROM platos
            WHERE %s = TRUE AND activo = TRUE
            ORDER BY id
            LIMIT 10
            """,
            (restriccion,)
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
            INSERT INTO platos (nombre, descripcion, precio, vegano, vegetariano, gluten, imagen_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                plato_data["nombre"],
                plato_data.get("descripcion", ""),
                plato_data["precio"],
                plato_data.get("vegano", False),
                plato_data.get("vegetariano", False),
                plato_data.get("gluten", False),
                plato_data.get("imagen_url", "")
            )
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
            UPDATE platos
            SET nombre = %s, descripcion = %s, precio = %s, vegano = %s, vegetariano = %s, gluten = %s, imagen_url = %s
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
                id
            )
        )
        conn.commit()
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
            UPDATE platos
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