class Config:
    # para tokens personalizados 
    SECRET_KEY= 'grYTYG4#jsjs'
class DevelopmentConfig(Config):
    DEBUG = True 

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}