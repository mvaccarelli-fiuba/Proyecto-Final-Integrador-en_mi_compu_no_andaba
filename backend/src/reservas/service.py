from src.reservas import repository

def get_disponibilidad(cantidad_personas):
    return repository.get_disponibilidad(cantidad_personas)
