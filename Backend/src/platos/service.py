from src.platos import repository


def get_platos():
    return repository.get_all_platos()

def get_plato(id):
    return repository.get_plato(id)

def get_platos_con_restriccion(restriccion):
    return repository.get_platos_con_restriccion(restriccion)

def create_plato(plato_data):
    return repository.create_plato(plato_data)

def update_plato(id, plato_data):
    return repository.update_plato(id, plato_data)

def delete_plato(id):
    return repository.delete_plato(id)