from flask import jsonify


def error(codigo, mensaje, descripcion, codigo_estatus):
    """
    Devuelve una respuesta de error con formato consistente para toda la API.

    """
    return (
        jsonify(
            {
                "errors": [
                    {
                        "code": codigo,
                        "message": mensaje,
                        "level": "error",
                        "description": descripcion,
                    }
                ]
            }
        ),
        codigo_estatus,
    )
