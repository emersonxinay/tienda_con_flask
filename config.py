from decouple import config
class Config:
    # para tokens personalizados 
    SECRET_KEY= 'grYTYG4#jsjs'
class DevelopmentConfig(Config):
    DEBUG = True 
    MYSQL_HOST = 'localhost'
    MYSQL_USER ='root'
    MYSQL_PASSWORD = ''
    MYSQL_DB= 'tienda'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587  # TLS: Transport Layer Security: Seguridad de la capa de transporte
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'compilandocode@gmail.com'
    MAIL_PASSWORD = config('MAIL_PASSWORD')
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
