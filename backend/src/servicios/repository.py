import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_table():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS servicio_extra (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(80) NOT NULL UNIQUE,
                descripcion VARCHAR(255),
                activo BOOLEAN NOT NULL DEFAULT TRUE
            )
            """
        )
        conn.commit()
        cursor.close()
    finally:
        if conn.is_connected():
            conn.close()


def get_all_servicios():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nombre, descripcion
            FROM servicio_extra
            WHERE activo = TRUE
            ORDER BY id
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def create_servicio(data):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO servicio_extra (nombre, descripcion)
            VALUES (%s, %s)
            """,
            (data["nombre"], data.get("descripcion", ""))
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return get_servicio(new_id)
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def update_servicio(id, data):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE servicio_extra
            SET nombre = %s, descripcion = %s
            WHERE id = %s AND activo = TRUE
            """,
            (data["nombre"], data.get("descripcion", ""), id)
        )
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        if affected == 0:
            raise ValueError(f"Servicio {id} no encontrado")
        return get_servicio(id)
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()


def get_servicio(id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nombre, descripcion
            FROM servicio_extra
            WHERE id = %s
            """,
            (id,)
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return row
        raise ValueError(f"Servicio {id} no encontrado")
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()
