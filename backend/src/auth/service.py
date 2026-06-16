from werkzeug.security import check_password_hash
from src.auth import repository


def login(email, password):
    admin = repository.get_admin_por_email(email)
    if not admin:
        return None

    # chequeamos la contraseña hasheada de la bd con lo ingresado por el usuario(tambien se hashea)
    if not check_password_hash(admin["password_hash"], password):
        return None

    # Devolvemos los datos sin el hash
    return {
        "id": admin["id"],
        "email": admin["email"],
        "nombre": admin["nombre"],
    }
