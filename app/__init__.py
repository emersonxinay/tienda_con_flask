from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user
from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import ModeloUsuario
from .models.entities.Usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash


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
@app.route("/")
def index():
    return render_template('index.html')
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
            
            return redirect(url_for('index'))
        else:
            flash("Credenciales invalidas...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
@app.route('/logout')
def logout():
    logout_user()
    flash('Cerraste sesión exitosamente.')
    return redirect(url_for('login'))


# # rutas para probar base de datos 
# @app.route('/libros')
# def listar_libros():
#     try:
#         cursor = db.connection.cursor()
#         sql = "SELECT LIB.isbn, LIB.titulo, LIB.anioedicion, LIB.precio, AUT.apellidos, AUT.nombres FROM libro LIB JOIN autor AUT ON LIB.autor_id = AUT.id ORDER BY LIB.titulo ASC"
#         cursor.execute(sql)
#         data = cursor.fetchall()
#         data = {
#             "libros":data
#         }
#         return render_template('listado_libros.html', data=data)

#     except Exception as ex:
#         raise Exception(ex)

@app.route('/libros')
def listar_libros():
    try:
        libros = ModeloLibro.listar_libros(db)
        data = {
            'libros': libros
        }
        return render_template('listado_libros.html', libros=libros)

    except Exception as ex:
        print(ex)
        # return "Ocurrió un error"

# ruta para paginas no encontradas 
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)
    return app
