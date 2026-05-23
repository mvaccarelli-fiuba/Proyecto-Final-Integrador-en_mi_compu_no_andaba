from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "crusty-crab-secret-key"

@app.route("/")
def home():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)