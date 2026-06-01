from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "crusty-crab-secret-key"


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")


@app.route("/menu")
def menu():
    platos = []
    return render_template("menu.html", platos=platos)


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
def resenas():
    orden = request.args.get("orden", "recientes")
    resenas = []
    return render_template("resenas.html", resenas=resenas, orden=orden)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.errorhandler(404)
def pagina_no_encontrada():
    return render_template("error.html"), 404


@app.route("/reserva-confirmada")
def reserva_confirmada():
    return render_template("reserva_confirmada.html")


@app.route("/admin/menu")
def admin_menu():
    return render_template("admin_menu.html", seccion="menu")


@app.route("/admin/dashboard")
def admin_dashboard():
    # TODO: armar plantilla admin_dashboard.html
    return "<h1>Dashboard (TODO)</h1>"


@app.route("/admin/reservas")
def admin_reservas():
    # TODO: armar plantilla admin_reservas.html
    return "<h1>Reservas admin (TODO)</h1>"


@app.route("/admin/mesas")
def admin_mesas():
    # TODO: armar plantilla admin_mesas.html
    return "<h1>Mesas (TODO)</h1>"


@app.route("/admin/servicios")
def admin_servicios():
    # TODO: armar plantilla admin_servicios.html
    return "<h1>Servicios admin (TODO)</h1>"


@app.route("/admin/qr")
def admin_qr():
    # TODO: armar plantilla admin_qr.html
    return "<h1>Validar QR (TODO)</h1>"


@app.route("/admin/logout")
def admin_logout():
    # TODO: cuando este integrado al backend, hacer fetch POST /auth/logout.
    return "<h1>Logout (TODO)</h1>"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
