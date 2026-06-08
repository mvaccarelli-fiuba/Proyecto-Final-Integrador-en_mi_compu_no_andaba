import os
import qrcode

# Carpeta donde se guardan los QRs generados
QR_DIR = os.path.join("static", "qrs")


def generar_qr(token):
    """
    Genera un QR a partir del token de la reserva y lo guarda como PNG.
    Devuelve la ruta relativa al archivo (ej: '/static/qrs/abc-123.png').
    """
    # Asegurarse de que la carpeta exista
    os.makedirs(QR_DIR, exist_ok=True)

    # Generar el QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(token)
    qr.make(fit=True)

    # Crear la imagen
    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar el archivo
    nombre_archivo = f"{token}.png"
    ruta_completa = os.path.join(QR_DIR, nombre_archivo)
    img.save(ruta_completa)

    # Devolver la URL relativa para que el frontend pueda mostrarla
    return f"/static/qrs/{nombre_archivo}"
