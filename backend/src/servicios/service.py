from src.servicios import repository


def get_servicios():
    return repository.get_all_servicios()


def create_servicio(data):
    return repository.create_servicio(data)


def update_servicio(id, data):
    return repository.update_servicio(id, data)
