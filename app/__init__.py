from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from .models.entities.Usuario import Usuario
from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import ModeloUsuario

app = Flask(__name__)
# protección para ataques
csrf = CSRFProtect()
# conecta la  base de datos 
db= MySQL(app)
# rutas
@app.route("/")
def index():
    return render_template('index.html')
# generar encriptación de  password
@app.route('/password/<password>')


# ruta para login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    """
    print(request.method)
    print(request.form['usuario'])
    print(request.form['password'])
    """
    if request.method=='POST':
        # print(request.form['usuario'])
        # print(request.form['password'])
        # return 'ok'
        usuario = Usuario(None, request.form['usuario'], request.form['password'], None)
        usuario_logeado = ModeloUsuario.login(db, usuario)
        if usuario_logeado != None :
            return redirect(url_for('index'))
        else:
            
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

# rutas para probar base de datos 
@app.route('/libros')
def listar_libros():
    try:
        libros= ModeloLibro.listar_libros(db)
        data={
            'libros':libros
        }
        return render_template('listado_libros.html', data=data)

    except Exception as ex:
        print(ex) 

# ruta para paginas no encontradas 
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)
    return app
