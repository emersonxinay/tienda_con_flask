from flask import Flask, render_template

app = Flask(__name__)
# rutas
@app.route("/")
def index():
    return "Hola mundo con compilando!!"
# ruta para paginas no encontradas 
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

def inicializar_app(config):
    app.config.from_object(config)
    app.register_error_handler(404, pagina_no_encontrada)
    return app
