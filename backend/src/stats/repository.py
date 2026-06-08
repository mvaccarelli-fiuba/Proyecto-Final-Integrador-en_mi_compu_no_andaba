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


def get_stats_reservas(periodo="meses"):
    """
    Agrupa la cantidad de reservas por período.
    periodo: 'dias' | 'semanas' | 'meses'
    Retorna los últimos N períodos con su cantidad.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        if periodo == "dias":
            cursor.execute(
            """
            SELECT
                periodo,
                DATE_FORMAT(STR_TO_DATE(periodo, '%Y-%m-%d'), '%d/%m') AS etiqueta,
                total
            FROM (
                SELECT
                    DATE_FORMAT(fecha, '%Y-%m-%d') AS periodo,
                    COUNT(*) AS total
                FROM reserva
                WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY DATE_FORMAT(fecha, '%Y-%m-%d')
            ) AS agrupado
            ORDER BY periodo ASC
            """
                )
        elif periodo == "semanas":
            cursor.execute(
            """
            SELECT
                periodo,
                CONCAT('Sem ', semana, ' (', anio, ')') AS etiqueta,
                total
            FROM (
                SELECT
                    CONCAT(YEAR(MIN(fecha)), '-W', LPAD(WEEK(MIN(fecha), 1), 2, '0')) AS periodo,
                    YEAR(MIN(fecha)) AS anio,
                    WEEK(MIN(fecha), 1) AS semana,
                    COUNT(*) AS total
                FROM reserva
                WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 12 WEEK)
                GROUP BY YEAR(fecha), WEEK(fecha, 1)
            ) AS agrupado
            ORDER BY periodo ASC
            """
                        )
        else:  # meses (default)
            cursor.execute(
            """
            SELECT
                periodo,
                DATE_FORMAT(STR_TO_DATE(CONCAT(periodo, '-01'), '%Y-%m-%d'), '%b %Y') AS etiqueta,
                total
            FROM (
                SELECT
                    DATE_FORMAT(fecha, '%Y-%m') AS periodo,
                    COUNT(*) AS total
                FROM reserva
                WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
                GROUP BY DATE_FORMAT(fecha, '%Y-%m')
            ) AS agrupado
            ORDER BY periodo ASC
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


def get_stats_cancelaciones():
    """
    Devuelve el Top 5 de clientes con más cancelaciones de reservas.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                cliente_nombre,
                cliente_email,
                COUNT(*) AS total_cancelaciones
            FROM reserva
            WHERE estado = 'cancelada'
            GROUP BY cliente_email, cliente_nombre
            ORDER BY total_cancelaciones DESC
            LIMIT 5
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


def get_stats_ocupacion():
    """
    Calcula el porcentaje de ocupación:
    mesas con al menos una reserva confirmada HOY / total de mesas activas.
    También devuelve el total de mesas y las reservadas.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM mesa WHERE activa = TRUE) AS total_mesas,
                (
                    SELECT COUNT(DISTINCT mesa_id)
                    FROM reserva
                    WHERE estado = 'confirmada'
                    AND fecha = CURDATE()
                ) AS mesas_reservadas_hoy
            """
        )
        row = cursor.fetchone()
        cursor.close()

        total = row["total_mesas"] or 0
        reservadas = row["mesas_reservadas_hoy"] or 0
        porcentaje = round((reservadas / total * 100), 1) if total > 0 else 0.0

        return {
            "total_mesas": total,
            "mesas_reservadas_hoy": reservadas,
            "mesas_libres_hoy": total - reservadas,
            "porcentaje_ocupacion": porcentaje,
        }
    except mysql.connector.Error:
        raise
    finally:
        if conn.is_connected():
            conn.close()
