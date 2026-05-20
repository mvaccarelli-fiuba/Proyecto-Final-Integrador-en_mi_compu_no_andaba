import os

# bd_lucas
"""DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "TuContraseña123!",
    "database": "crusty_crab",
}
"""

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "tp_user",
    "password": "1234",
    "database": "crusty_crab",
}

SECRET_KEY = "dev-secret-key-change-in-production"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLATOS_IMAGES_DIR = os.path.join(BASE_DIR, "static", "platos")
PLATOS_IMAGES_URL_PREFIX = "/static/platos"
