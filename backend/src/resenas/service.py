from src.resenas import repository


def get_resenas():
    return repository.get_all_resenas()


def get_resena(id):
    return repository.get_resena(id)


def create_resena(resena_data):
    return repository.create_resena(resena_data)


def delete_resena(id):
    return repository.delete_resena(id)