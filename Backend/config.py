import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "krusty_user"),
    "password": os.getenv("DB_PASSWORD", "krusty_pass"),
    "database": os.getenv("DB_NAME", "krusty_krab"),
}
