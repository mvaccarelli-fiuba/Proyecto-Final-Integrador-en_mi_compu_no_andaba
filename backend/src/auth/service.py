from src.auth import repository


def login(email, password):
    admin = repository.get_admin_por_email(email)

    if admin is None:
        return None

    # TODO: hashear con werkzeug.security.
    # Cambiar por: from werkzeug.security import check_password_hash
    # if not check_password_hash(admin["password_hash"], password): return None

    if admin["password_hash"] != password:
        return None

    if not admin["activo"]:
        return None

    # No devolvemos
    return {
        "id": admin["id"],
        "email": admin["email"],
        "nombre": admin["nombre"],
    }
