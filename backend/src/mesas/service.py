from src.mesas import repository


def get_mesas():
    return repository.get_all_mesas()


def get_mesa(id):
    return repository.get_mesa(id)


def create_mesa(mesa_data):
    return repository.create_mesa(mesa_data)


def update_mesa(id, mesa_data):
    return repository.update_mesa(id, mesa_data)


def delete_mesa(id):
    return repository.delete_mesa(id)
