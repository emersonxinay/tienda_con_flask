from werkzeug.security import check_password_hash
from .entities.Usuario import Usuario
class ModeloUsuario():
    def login(self, db, usuario):
        try:
            cursor=db.conection.cursor()
            sql=f"SELECT id, usuario, password FROM usuario WHERE usuario ={usuario.usuario}"
            cursor.execute(sql)
            data = cursor.fetchall()
            # print(data)
            coincide = check_password_hash(data[2], usuario.password)
            if coincide:
                usuario_logeado = Usuario(data[0], None, None)
                return usuario_logeado
            else:

                return None
        except Exception as ex:
            raise Exception(ex)