from src.resenas import repository


def get_resenas():
    return repository.get_all_resenas()


def create_resena(resena_data):
    token = resena_data.get("token")
    puntaje = resena_data.get("estrellas") or resena_data.get("puntaje")
    comentario = resena_data.get("comentario")

    # Validaciones
    if not token:
        raise ValueError("Token requerido")
    if not puntaje or int(puntaje) < 1 or int(puntaje) > 5:
        raise ValueError("Puntaje debe estar entre 1 y 5")
    if not comentario or not comentario.strip():
        raise ValueError("El comentario es obligatorio")

    # Buscar la reserva
    reserva = repository.get_reserva_por_token(token)
    if not reserva:
        raise ValueError("Reserva no encontrada")

    # La reserva debe estar consumida
    if reserva["estado"] != "consumida":
        raise ValueError("Solo se puede reseñar una reserva consumida")

    # No puede haber dos reseñas para la misma reserva
    if repository.existe_resena_para_reserva(reserva["id"]):
        raise ValueError("Ya existe una reseña para esta reserva")

    # Crear la reseña
    nueva_resena = {
        "reserva_id": reserva["id"],
        "nombre": reserva["cliente_nombre"],
        "estrellas": int(puntaje),
        "comentario": comentario.strip(),
    }
    return repository.create_resena(nueva_resena)


def delete_resena(id):
    return repository.delete_resena(id)
