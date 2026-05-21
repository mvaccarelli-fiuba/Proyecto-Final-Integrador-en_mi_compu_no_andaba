import random
from src.reservas import repository


def get_disponibilidad(cantidad_personas):
    return repository.get_disponibilidad(cantidad_personas)


def create_reserva(reserva_data):
    token = str(random.randint(100000, 999999))
    reserva_data["token"] = token
    nueva_reserva = repository.create_reserva(reserva_data)

    return {
        "id": nueva_reserva,
        "token": token
    }


def get_reserva(token):
    return repository.get_reserva(token)


def cancelar_reserva(token):
    return repository.cancelar_reserva(token)
