from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import ModeloUsuario
from .models.entities.Usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from .consts import * 

app = Flask(__name__)
# protección para ataques
csrf = CSRFProtect()
# conecta la  base de datos 
db= MySQL(app)

login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db, id)

    

# rutas

# generar encriptación de  password
@app.route('/password/<password>')
def generar_password(password):
    encriptado =generate_password_hash(password)
    valor = check_password_hash(encriptado, password)
    return "encriptado: {0} | coincide: {1} ".format(encriptado, valor)


# ruta para login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method=='POST':
        
        usuario = Usuario(None, request.form['usuario'], request.form['password'], None)
        usuario_logeado = ModeloUsuario.login(db, usuario)
        if usuario_logeado != None :
            login_user(usuario_logeado)
            flash(MENSAJE_BIENVENIDA, 'success')
            return redirect(url_for('index'))
        else:
            flash(LOGIN_CREDENTIALSINVALIDAS, 'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            libros_vendidos = []
            data = {
                'titulo': 'Libros Vendidos',
                'libros_vendidos': libros_vendidos

            }
        else:
            compras = []
            data = {
                'titulo': 'Mis compras',
                'compras': compras

            }
        return render_template('index.html', data = data)
    else:
        return redirect(url_for('login'))
@app.route('/libros')
@login_required
def listar_libros():
    try:
        libros = ModeloLibro.listar_libros(db)
        data = {
            'titulo': 'Listado de libros',
            'libros': libros
        }
        return render_template('listado_libros.html', data=data)
    except Exception as ex:
        return render_template('errores/error.html', mensaje=format(ex))

# ruta para paginas no encontradas 
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

def pagina_no_autorizada(error):
    return redirect(url_for('login'))

def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    app.register_error_handler(401, pagina_no_autorizada)
    app.register_error_handler(404, pagina_no_encontrada)
    return app
