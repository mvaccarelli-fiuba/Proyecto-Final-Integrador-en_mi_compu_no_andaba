import os
import smtplib
from email.message import EmailMessage

from config import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    EMAIL_FROM_NAME,
)


def enviar_email_reserva(reserva, qr_path):
    """
    Envía un mail al cliente con los datos de su reserva y el QR adjunto.

    Args:
        reserva (dict): datos de la reserva (cliente_nombre, cliente_email,
                        token, fecha, hora_inicio, cantidad_personas, etc.)
        qr_path (str): ruta relativa del QR, ej: '/static/qrs/abc.png'
    """
    msg = EmailMessage()
    msg["Subject"] = f"Reserva confirmada - Krusty Krab"
    msg["From"] = f"{EMAIL_FROM_NAME} <{EMAIL_USER}>"
    msg["To"] = reserva["cliente_email"]

    # Cuerpo del mail en texto plano
    cuerpo_texto = f"""
Hola {reserva["cliente_nombre"]},

¡Tu reserva en Krusty Krab está confirmada!

Detalles:
- Fecha: {reserva["fecha"]}
- Hora: {reserva["hora_inicio"]}
- Personas: {reserva["cantidad_personas"]}
- Token de reserva: {reserva["token"]}

Te adjuntamos el QR de tu reserva. Mostralo al llegar al local para validar tu mesa.

¡Te esperamos!
Krusty Krab
"""
    msg.set_content(cuerpo_texto)

    # Cuerpo HTML (versión más linda)
    cuerpo_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; color: #042C53;">
    <h2 style="color: #185FA5;">¡Tu reserva está confirmada! 🦀</h2>
    <p>Hola <strong>{reserva["cliente_nombre"]}</strong>,</p>
    <p>Te esperamos en Krusty Krab. Acá están los detalles:</p>

    <table style="border-collapse: collapse; margin: 20px 0;">
      <tr><td style="padding: 6px 12px;"><strong>Fecha:</strong></td><td>{reserva["fecha"]}</td></tr>
      <tr><td style="padding: 6px 12px;"><strong>Hora:</strong></td><td>{reserva["hora_inicio"]}</td></tr>
      <tr><td style="padding: 6px 12px;"><strong>Personas:</strong></td><td>{reserva["cantidad_personas"]}</td></tr>
    </table>

    <p>Adjuntamos el <strong>QR de tu reserva</strong>. Mostralo al llegar al local.</p>

    <p style="margin-top: 30px; color: #5F5E5A; font-size: 12px;">
      Token: {reserva["token"]}<br>
      ¡Te esperamos!
    </p>
  </body>
</html>
"""
    msg.add_alternative(cuerpo_html, subtype="html")

    # Adjuntar el QR si existe
    ruta_local_qr = qr_path.lstrip("/")  # quita el "/" inicial
    if os.path.exists(ruta_local_qr):
        with open(ruta_local_qr, "rb") as f:
            qr_bytes = f.read()
        msg.add_attachment(
            qr_bytes,
            maintype="image",
            subtype="png",
            filename=f"reserva-{reserva['token'][:8]}.png",
        )

    # Conectar al SMTP y mandar
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.starttls()  # cifrado TLS
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except smtplib.SMTPException as e:
        print(f"[ERROR] No se pudo enviar el mail: {e}")
        return False
