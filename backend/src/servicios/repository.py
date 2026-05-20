import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


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
