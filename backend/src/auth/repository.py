import mysql.connector
from config import DB_CONFIG


def get_admin_por_email(email):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, email, password_hash, nombre, activo FROM admin WHERE email = %s",
        (email,),
    )
    admin = cursor.fetchone()

    cursor.close()
    conn.close()
    return admin
