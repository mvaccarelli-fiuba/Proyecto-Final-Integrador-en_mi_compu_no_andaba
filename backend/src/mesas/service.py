from src.mesas import repository


def get_all_mesas():
    return repository.get_all_mesas()


def get_mesa(id):
    return repository.get_mesa(id)


def create_mesa(mesa_data):
    # Validaciones básicas
    if not mesa_data.get("numero"):
        raise ValueError("El número de mesa es requerido")
    if not mesa_data.get("capacidad"):
        raise ValueError("La capacidad es requerida")
    if int(mesa_data["capacidad"]) < 1:
        raise ValueError("La capacidad debe ser al menos 1")
    if int(mesa_data["numero"]) < 1:
        raise ValueError("El número de mesa debe ser positivo")

    return repository.create_mesa(mesa_data)


def update_mesa(id, mesa_data):
    if not mesa_data.get("numero"):
        raise ValueError("El número de mesa es requerido")
    if not mesa_data.get("capacidad"):
        raise ValueError("La capacidad es requerida")
    if int(mesa_data["capacidad"]) < 1:
        raise ValueError("La capacidad debe ser al menos 1")

    return repository.update_mesa(id, mesa_data)


def delete_mesa(id):
    return repository.delete_mesa(id)
