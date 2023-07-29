from flask import Flask

app = Flask(__name__)
# rutas
@app.route("/")
def index():
    return "Hola mundo con compilando!!"


def inicializar_app(config):
    app.config.from_object(config)
    return app
