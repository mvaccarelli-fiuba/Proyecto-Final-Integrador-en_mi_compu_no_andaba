from src.stats import repository

PERIODOS_VALIDOS = {"dias", "semanas", "meses"}


def get_stats_reservas(periodo="meses"):
    if periodo not in PERIODOS_VALIDOS:
        raise ValueError(
            f"El parámetro 'periodo' debe ser uno de: {', '.join(PERIODOS_VALIDOS)}"
        )   
    return repository.get_stats_reservas(periodo)
    
def get_stats_cancelaciones():
    return repository.get_stats_cancelaciones()

def get_stats_ocupacion():
    return repository.get_stats_ocupacion()
