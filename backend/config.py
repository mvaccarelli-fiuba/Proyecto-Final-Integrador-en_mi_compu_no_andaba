import os

# bd_lucas
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "tp_user"),
    "password": os.getenv("DB_PASSWORD", "1234"),
    "database": os.getenv("DB_NAME", "crusty_crab"),
}

"""
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "tp_user",
    "password": "1234",
    "database": "crusty_crab",
}"""

SECRET_KEY = "dev-secret-key-change-in-production"

##email:crustycrabtp@gmail.com
##contraseña:#grupo-20-en_mi_compu_andaba
##contraseña para la aplicacion del dispositivo : crvb qxdz ydvq mnmz


# Configuración de email (Gmail SMTP)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "crustycrabtp@gmail.com"  # mail generador
EMAIL_PASSWORD = "crvb qxdz ydvq mnmz"  # password de aplicación (16 chars)
EMAIL_FROM_NAME = "Krusty Krab Reservas"
