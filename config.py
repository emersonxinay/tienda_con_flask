class Config:
    # para tokens personalizados 
    SECRET_KEY= 'grYTYG4#jsjs'
class DevelopmentConfig(Config):
    DEBUG = True 
    MYSQL_HOST = 'localhost'
    MYSQL_USER ='root'
    MYSQL_PASSWORD = ''
    MYSQL_DB= 'tienda'
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}