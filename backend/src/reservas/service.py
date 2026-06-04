import uuid
from src.reservas import repository


def get_disponibilidad(cantidad_personas, fecha):
    return repository.get_disponibilidad(cantidad_personas, fecha)


def create_reserva(reserva_data):
    token = str(uuid.uuid4())
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

def consumir_reserva(token):
    return repository.consumir_reserva(token)


def get_reservas(estado=None, fecha=None):
    return repository.get_reservas(estado, fecha)
