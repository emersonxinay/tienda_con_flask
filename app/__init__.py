from flask import Flask

app = Flask(__name__)
# rutas
@app.route('/')
def index():
    return "Hola mundo!!"
def inicializar_app():
    return app
