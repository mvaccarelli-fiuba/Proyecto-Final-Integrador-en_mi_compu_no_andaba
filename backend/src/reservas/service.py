import uuid
from src.reservas import repository
from src.reservas.qr_service import generar_qr
from src.reservas.email_service import enviar_email_reserva, enviar_email_resena


def get_disponibilidad(cantidad_personas, fecha):
    return repository.get_disponibilidad(cantidad_personas, fecha)


def create_reserva(reserva_data):
    token = str(uuid.uuid4())
    reserva_data["token"] = token

    nueva_reserva_id = repository.create_reserva(reserva_data)
    ruta_qr = generar_qr(token)

    # Intentar mandar el mail. Si falla, la reserva igual queda creada.
    email_enviado = enviar_email_reserva(reserva_data, ruta_qr)

    return {
        "id": nueva_reserva_id,
        "token": token,
        "qr": ruta_qr,
        "email_enviado": email_enviado,
    }


def get_reserva(token):
    return repository.get_reserva(token)


def cancelar_reserva(token):
    return repository.cancelar_reserva(token)


def consumir_reserva(token):
    # Primero traemos la reserva para saber el email del cliente
    reserva = repository.get_reserva(token)

    # Después la consumimos
    repository.consumir_reserva(token)

    # Y mandamos el mail invitando a reseñar
    from src.reservas.email_service import enviar_email_resena

    enviar_email_resena(reserva)


def get_reservas(estado=None, fecha=None):
    return repository.get_reservas(estado, fecha)
