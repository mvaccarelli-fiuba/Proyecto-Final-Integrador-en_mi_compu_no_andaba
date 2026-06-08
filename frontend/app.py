from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)

from src import api_client
from src.utils import require_admin
from datetime import date

app = Flask(__name__)
app.secret_key = "crusty-crab-frontend"


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template("login.html", error="Completá email y contraseña.")

        # Llamar al backend
        response = api_client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )

        if response is None:
            return render_template(
                "login.html",
                error="No pudimos conectarnos al servidor. Probá de nuevo.",
            )

        if response.status_code == 200:
            # Login exitoso: guardamos cookie del backend + datos del admin.
            cookie = api_client.extract_session_cookie(response)
            session["backend_session_cookie"] = cookie
            session["admin"] = response.json()["admin"]
            return redirect(url_for("admin_menu"))

        if response.status_code == 401:
            return render_template("login.html", error="Credenciales inválidas.")

        return render_template(
            "login.html", error="Ocurrió un error al iniciar sesión."
        )

    return render_template("login.html", error=None)


@app.route("/admin/logout")
def admin_logout():
    # Avisamos al backend para que cierre la sesión también
    api_client.post("/auth/logout")
    # Limpiamos la sesión del frontend
    session.clear()
    return redirect(url_for("inicio"))


@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")


##-------------------------------------------------------FUNCIONES MENU------------------------------------------------------
@app.route("/menu")
def menu_publico():
    restriccion = request.args.get("restriccion")

    if restriccion:
        path = f"/platos?restriccion={restriccion}"
    else:
        path = "/platos"

    response = api_client.get(path)

    if response is None:
        return render_template(
            "menu.html",
            platos=[],
            filtro_activo=restriccion,
            error="No pudimos cargar el menú. Probá de nuevo en un rato.",
        )

    if response.status_code == 200:
        platos = response.json()
    else:
        platos = []

    return render_template(
        "menu.html",
        platos=platos,
        filtro_activo=restriccion,
        error=None,
    )


@app.route("/admin/menu")
@require_admin
def admin_menu():
    response = api_client.get("/platos")

    if response is None:
        return render_template(
            "admin_menu.html",
            seccion="menu",
            platos=[],
            error="No pudimos cargar el menú. Probá de nuevo en un rato.",
        )

    if response.status_code == 200:
        platos = response.json()
    else:
        platos = []

    return render_template(
        "admin_menu.html",
        seccion="menu",
        platos=platos,
        error=None,
    )


@app.route("/admin/menu/nuevo", methods=["POST"])
@require_admin
def admin_menu_nuevo():
    plato_data = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion") or "",
        "precio": float(request.form.get("precio") or 0),
        "imagen_url": request.form.get("imagen_url") or "",
        "vegetariano": "vegetariano" in request.form,
        "vegano": "vegano" in request.form,
        "gluten": "gluten" in request.form,
    }

    response = api_client.post("/platos", json=plato_data)

    if response is None:
        flash("Error de conexión con el backend.", "error")
    elif response.status_code == 201:
        flash(f"Plato '{plato_data['nombre']}' creado correctamente.", "exito")
    else:
        flash("No se pudo crear el plato. Revisá los datos.", "error")

    return redirect(url_for("admin_menu"))


@app.route("/admin/menu/<int:id>/editar", methods=["POST"])
@require_admin
def admin_menu_editar(id):
    plato_data = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion") or "",
        "precio": float(request.form.get("precio") or 0),
        "imagen_url": request.form.get("imagen_url") or "",
        "vegetariano": "vegetariano" in request.form,
        "vegano": "vegano" in request.form,
        "gluten": "gluten" in request.form,
    }

    response = api_client.put(f"/platos/{id}", json=plato_data)

    if response is None:
        flash("Error de conexión con el backend.", "error")
    elif response.status_code == 200:
        flash(f"Plato '{plato_data['nombre']}' actualizado.", "exito")
    elif response.status_code == 404:
        flash("Ese plato no existe.", "error")
    else:
        flash("No se pudo actualizar el plato.", "error")

    return redirect(url_for("admin_menu"))


@app.route("/admin/menu/<int:id>/borrar", methods=["POST"])
@require_admin
def admin_menu_borrar(id):
    response = api_client.delete(f"/platos/{id}")

    if response is None:
        flash("Error de conexión con el backend.", "error")
    elif response.status_code in (200, 204):
        flash("Plato eliminado.", "exito")
    elif response.status_code == 404:
        flash("Ese plato no existe.", "error")
    else:
        flash("No se pudo eliminar el plato.", "error")

    return redirect(url_for("admin_menu"))


##-------------------------------------------------------FUNCIONES MESAS------------------------------------------------------


@app.route("/admin/mesas")
@require_admin
def admin_mesas():
    response = api_client.get("/mesas")

    if response is None:
        return render_template(
            "admin_mesas.html",
            seccion="mesas",
            mesas=[],
            error="No pudimos cargar las mesas. Probá de nuevo en un rato.",
        )

    if response.status_code == 200:
        mesas = response.json()
    else:
        # 204 = no hay mesas; otro código también cae acá.
        mesas = []

    return render_template(
        "admin_mesas.html",
        seccion="mesas",
        mesas=mesas,
        error=None,
    )


@app.route("/admin/mesas/nuevo", methods=["POST"])
@require_admin
def admin_mesas_nuevo():
    mesa_data = {
        "numero": int(request.form.get("numero") or 0),
        "capacidad": int(request.form.get("capacidad") or 0),
        "activa": "activa" in request.form,
    }

    response = api_client.post("/mesas", json=mesa_data)

    if response is None:
        flash("Error de conexión con el backend.", "error")
    elif response.status_code == 201:
        flash(f"Mesa #{mesa_data['numero']} creada correctamente.", "exito")
    elif response.status_code == 409:
        flash(f"Ya existe una mesa con el número {mesa_data['numero']}.", "error")
    elif response.status_code == 400:
        flash("Datos inválidos. Revisá el número y la capacidad.", "error")
    else:
        flash("No se pudo crear la mesa.", "error")

    return redirect(url_for("admin_mesas"))


@app.route("/admin/mesas/<int:id>/editar", methods=["POST"])
@require_admin
def admin_mesas_editar(id):
    mesa_data = {
        "numero": int(request.form.get("numero") or 0),
        "capacidad": int(request.form.get("capacidad") or 0),
        "activa": "activa" in request.form,
    }

    response = api_client.put(f"/mesas/{id}", json=mesa_data)

    if response is None:
        flash("Error de conexión con el backend.", "error")
    elif response.status_code == 200:
        flash(f"Mesa #{mesa_data['numero']} actualizada.", "exito")
    elif response.status_code == 404:
        flash("Esa mesa no existe.", "error")
    elif response.status_code == 409:
        flash(f"Ya existe otra mesa con el número {mesa_data['numero']}.", "error")
    else:
        flash("No se pudo actualizar la mesa.", "error")

    return redirect(url_for("admin_mesas"))


@app.route("/admin/mesas/<int:id>/borrar", methods=["POST"])
@require_admin
def admin_mesas_borrar(id):
    response = api_client.delete(f"/mesas/{id}")

    if response is None:
        flash("Error de conexión con el backend.", "error")
    elif response.status_code in (200, 204):
        flash("Mesa dada de baja.", "exito")
    elif response.status_code == 404:
        flash("Esa mesa no existe.", "error")
    else:
        flash("No se pudo dar de baja la mesa.", "error")

    return redirect(url_for("admin_mesas"))


##-------------------------------------------------------FUNCIONES RESERVAS------------------------------------------------------


@app.route("/reservas", methods=["GET", "POST"])
def reservas():
    if request.method == "POST":
        reserva_data = {
            "cliente_nombre": request.form.get("cliente_nombre"),
            "cliente_email": request.form.get("cliente_email"),
            "cantidad_personas": int(request.form.get("cantidad_personas") or 0),
            "fecha": request.form.get("fecha"),
            "hora_inicio": request.form.get("hora_inicio"),
        }

        # Validación básica antes de pegarle al backend
        campos_vacios = [k for k, v in reserva_data.items() if not v]
        if campos_vacios:
            return render_template(
                "reservas.html",
                error="Completá todos los campos del formulario.",
                mensaje_exito=None,
            )

        response = api_client.post("/reservas", json=reserva_data)

        if response is None:
            return render_template(
                "reservas.html",
                error="No pudimos conectarnos al servidor. Probá de nuevo en un rato.",
                mensaje_exito=None,
            )

        if response.status_code == 201:
            return render_template(
                "reservas.html",
                error=None,
                mensaje_exito=f"¡Reserva confirmada! Te enviamos los detalles a {reserva_data['cliente_email']}.",
            )

        if response.status_code == 404:
            return render_template(
                "reservas.html",
                error="No hay mesas disponibles para esa fecha y cantidad de personas.",
                mensaje_exito=None,
            )

        return render_template(
            "reservas.html",
            error="No se pudo crear la reserva. Revisá los datos.",
            mensaje_exito=None,
        )

    # mostrar el form
    return render_template("reservas.html", error=None, mensaje_exito=None)


@app.route("/resenas")
def resenas_publicas():
    response = api_client.get("/resenas")

    if response is None:
        return render_template(
            "resenas.html",
            resenas=[],
            error="No pudimos cargar las reseñas. Probá de nuevo en un rato.",
        )

    if response.status_code == 200:
        resenas = response.json()
    else:
        # 204 = no hay reseñas todavía, también caemos acá si hay error.
        resenas = []

    return render_template("resenas.html", resenas=resenas, error=None)


@app.route("/reserva-confirmada")
def reserva_confirmada():
    return render_template("reserva_confirmada.html")


@app.route("/admin/reservas")
@require_admin
def admin_reservas():
    estado_filtro = request.args.get("estado")
    fecha_filtro = request.args.get("fecha")

    # Armamos los query params para el backend
    params = []
    if estado_filtro:
        params.append(f"estado={estado_filtro}")
    if fecha_filtro:
        params.append(f"fecha={fecha_filtro}")
    query = "?" + "&".join(params) if params else ""

    response = api_client.get(f"/admin/reservas{query}")

    if response is None:
        return render_template(
            "admin_reservas.html",
            seccion="reservas",
            reservas=[],
            resumen={"hoy": 0, "consumidas": 0, "canceladas": 0, "proxima": None},
            error="No pudimos cargar las reservas. Probá de nuevo en un rato.",
            estado_filtro=estado_filtro,
            fecha_filtro=fecha_filtro,
        )

    if response.status_code == 200:
        reservas = response.json()
    else:
        reservas = []

    # Calculamos métricas para las tarjetas de resumen
    resumen = calcular_resumen_reservas(reservas)

    return render_template(
        "admin_reservas.html",
        seccion="reservas",
        reservas=reservas,
        resumen=resumen,
        error=None,
        estado_filtro=estado_filtro,
        fecha_filtro=fecha_filtro,
    )


@app.route("/admin/reservas/consumir", methods=["POST"])
@require_admin
def admin_reservas_consumir():
    token = request.form.get("token")

    if not token:
        flash("Token vacío.", "error")
        return redirect(url_for("admin_reservas"))

    response = api_client.post("/admin/reservas/consumir", json={"token": token})

    if response is None:
        flash("Error de conexión con el backend.", "error")
    elif response.status_code == 200:
        flash("Reserva marcada como consumida.", "exito")
    elif response.status_code == 404:
        flash("Reserva no encontrada o ya consumida/cancelada.", "error")
    else:
        flash("No se pudo consumir la reserva.", "error")

    return redirect(url_for("admin_reservas"))


@app.route("/admin/reservas/cancelar", methods=["POST"])
@require_admin
def admin_reservas_cancelar():
    token = request.form.get("token")

    if not token:
        flash("Token vacío.", "error")
        return redirect(url_for("admin_reservas"))

    response = api_client.put(f"/reservas/{token}/cancelar")

    if response is None:
        flash("Error de conexión con el backend.", "error")
    elif response.status_code == 200:
        flash("Reserva cancelada.", "exito")
    elif response.status_code == 404:
        flash("Reserva no encontrada o ya cancelada.", "error")
    else:
        flash("No se pudo cancelar la reserva.", "error")

    return redirect(url_for("admin_reservas"))


def calcular_resumen_reservas(reservas):
    """Calcula métricas básicas a partir de la lista de reservas."""
    hoy = date.today().isoformat()
    reservas_hoy = [
        r for r in reservas if r.get("fecha") == hoy and r.get("estado") == "confirmada"
    ]
    consumidas = [r for r in reservas if r.get("estado") == "consumida"]
    canceladas = [r for r in reservas if r.get("estado") == "cancelada"]

    # Próxima reserva del día = la confirmada de hoy con hora más temprana que aún no pasó
    proxima = None
    if reservas_hoy:
        ordenadas = sorted(reservas_hoy, key=lambda r: r.get("hora_inicio") or "")
        proxima = ordenadas[0]

    return {
        "hoy": len(reservas_hoy),
        "consumidas": len(consumidas),
        "canceladas": len(canceladas),
        "proxima": proxima,
    }


@app.route("/cancelar/<token>")
def cancelar_reserva_view(token):
    """
    Muestra la pagina de confirmacion de cancelación.
    """
    response = api_client.get(f"/reservas/{token}")

    if response is None:
        return render_template(
            "cancelar_reserva.html",
            reserva=None,
            error="No pudimos conectarnos al servidor. Probá de nuevo en un rato.",
            cancelada=False,
        )

    if response.status_code == 404:
        return render_template(
            "cancelar_reserva.html",
            reserva=None,
            error="Esta reserva no existe o el link es inválido.",
            cancelada=False,
        )

    if response.status_code != 200:
        return render_template(
            "cancelar_reserva.html",
            reserva=None,
            error="No pudimos cargar la reserva.",
            cancelada=False,
        )

    reserva = response.json()

    # Solo permitir cancelar si esta confirmada
    if reserva.get("estado") != "confirmada":
        return render_template(
            "cancelar_reserva.html",
            reserva=reserva,
            error=f"Esta reserva ya está {reserva.get('estado')}, no se puede cancelar.",
            cancelada=False,
        )

    return render_template(
        "cancelar_reserva.html",
        reserva=reserva,
        error=None,
        cancelada=False,
    )


@app.route("/cancelar/<token>", methods=["POST"])
def cancelar_reserva_confirmar(token):
    """
    Procesa la confirmacion de cancelacion.
    """
    response = api_client.put(f"/reservas/{token}/cancelar")

    if response is None:
        return render_template(
            "cancelar_reserva.html",
            reserva=None,
            error="No pudimos conectarnos al servidor. Probá de nuevo.",
            cancelada=False,
        )

    if response.status_code == 200:
        return render_template(
            "cancelar_reserva.html",
            reserva=None,
            error=None,
            cancelada=True,
        )

    if response.status_code == 404:
        return render_template(
            "cancelar_reserva.html",
            reserva=None,
            error="Esta reserva no existe.",
            cancelada=False,
        )

    return render_template(
        "cancelar_reserva.html",
        reserva=None,
        error="No se pudo cancelar la reserva. Probá de nuevo o contactanos.",
        cancelada=False,
    )


@app.route("/admin/reservas/consumir-qr", methods=["POST"])
@require_admin
def admin_reservas_consumir_qr():
    """
    Endpoint para que la página de escaneo de QR consuma reservas.
    A diferencia de admin_reservas_consumir, este devuelve JSON
    en vez de redirigir.
    """
    token = request.form.get("token")

    if not token:
        return jsonify({"mensaje": "Token vacío"}), 400

    response = api_client.post("/admin/reservas/consumir", json={"token": token})

    if response is None:
        return jsonify({"mensaje": "No pudimos conectarnos al servidor"}), 503

    if response.status_code == 200:
        return jsonify({"mensaje": "Reserva consumida correctamente"}), 200

    if response.status_code == 404:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404

    # Otros casos (ya consumida, ya cancelada, etc.)
    try:
        backend_error = response.json()
        descripcion = backend_error.get("errors", [{}])[0].get(
            "description", "Error desconocido"
        )
    except Exception:
        descripcion = "No se pudo consumir la reserva"

    return jsonify({"mensaje": descripcion}), response.status_code


##-------------------------------------------------------FUNCIONES ------------------------------------------------------


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    return render_template("contacto.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.errorhandler(404)
def pagina_no_encontrada():
    return render_template("error.html"), 404


@app.route("/admin/servicios")
@require_admin
def admin_servicios():
    return render_template("admin_servicios.html", seccion="servicios")


@app.route("/admin/qr")
@require_admin
def admin_qr():
    return render_template(
        "admin_qr.html", seccion="qr", admin_email=session["admin"]["email"]
    )


@app.route("/admin/dashboard")
@require_admin
def admin_dashboard():
    # TODO: armar plantilla admin_dashboard.html
    return "<h1>Dashboard (TODO)</h1>"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
