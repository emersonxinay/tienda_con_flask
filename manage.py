from flask_script import Manager
from app import inicializar_app
app = inicializar_app()
manage = Manager(app)

if __name__ == "__main__":
    manage.run()
print("Hola mundo")