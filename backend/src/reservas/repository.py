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



def get_disponibilidad(cantidad_personas):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT *
            FROM mesa 
            WHERE capacidad >= %s
            AND activa = True
            """,
            (cantidad_personas,)
        )    
        
        rows = cursor.fetchall()
        cursor.close()
        return [convert_row_to_dict(row) for row in rows]
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()




            




