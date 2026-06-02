from flask import Flask

from config import SECRET_KEY
from src.auth.routes import auth_bp
from src.platos.routes import platos_bp
from src.resenas.routes import resenas_bp
from src.servicios.routes import servicios_bp
from src.mesas.routes import mesas_bp

# A medida que cada dominio se mergee a main, descomentar la linea.
# from src.reservas.routes import reservas_bp


app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(platos_bp)
app.register_blueprint(resenas_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(mesas_bp)

# app.register_blueprint(reservas_bp)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
