import os

DB_CONFIG = {
    # Host/dirección IP del servidor MySQL (localhost en desarrollo)
    "host": os.getenv("DB_HOST", "localhost"),

    # Puerto donde escucha MySQL (3306 es el puerto predeterminado)
    "port": int(os.getenv("DB_PORT", 3306)),

    # Usuario con permisos en la base de datos
    "user": os.getenv("DB_USER", "tp_user"),

    # Contraseña del usuario de base de datos
    "password": os.getenv("DB_PASSWORD", "1234"),

    # Nombre de la base de datos a usar (crusty_crab es la base de datos del proyecto)
    "database": os.getenv("DB_NAME", "crusty_crab"),
}


'''
DB_CONFIG = {
    "host": "db",
    "port": 3306,
    "user": "tp_user",
    "password": "1234",
    "database": "crusty_crab",
}
'''

SECRET_KEY = "dev-secret-key-change-in-production"

##email:crustycrabtp@gmail.com

##contraseña:#grupo-20-en_mi_compu_andaba
##contraseña para la aplicacion del dispositivo : crvb qxdz ydvq mnmz


# Configuración de email (Gmail SMTP)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "crustycrabtp@gmail.com"  # ← cambiar por tu mail
EMAIL_PASSWORD = "crvb qxdz ydvq mnmz"  # ← password de aplicación (16 chars)
EMAIL_FROM_NAME = "Krusty Krab Reservas"
