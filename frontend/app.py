from flask import Flask, render_template, request, redirect, url_for, session
from src import api_client
from src.utils import require_admin

app = Flask(__name__)
app.secret_key = "crusty-crab-frontend"


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")


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


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/reservas", methods=["GET", "POST"])
def reservas():
    return render_template("reservas.html")


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    return render_template("contacto.html")


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


@app.errorhandler(404)
def pagina_no_encontrada():
    return render_template("error.html"), 404


@app.route("/reserva-confirmada")
def reserva_confirmada():
    return render_template("reserva_confirmada.html")


@app.route("/admin/menu")
@require_admin
def admin_menu():
    return render_template("admin_menu.html", seccion="menu")


@app.route("/admin/dashboard")
@require_admin
def admin_dashboard():
    # TODO: armar plantilla admin_dashboard.html
    return "<h1>Dashboard (TODO)</h1>"


@app.route("/admin/reservas")
@require_admin
def admin_reservas():
    return render_template("admin_reservas.html", seccion="reservas")


@app.route("/admin/mesas")
@require_admin
def admin_mesas():
    return render_template("admin_mesas.html", seccion="mesas")


@app.route("/admin/servicios")
@require_admin
def admin_servicios():
    return render_template("admin_servicios.html", seccion="servicios")


@app.route("/admin/qr")
@require_admin
def admin_qr():
    # TODO: armar plantilla admin_qr.html
    return "<h1>Validar QR (TODO)</h1>"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
