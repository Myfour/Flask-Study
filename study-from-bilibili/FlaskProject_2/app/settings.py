# def config_app(app):
#     app.config[
#         'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'  #'sqlite:///sqlite.db'  # 这里uri设置  数据库+驱动://用户名:密码@主机:端口/库
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# from redis import Redis


def get_uri(dbinfo):
    uri = ''
    if dbinfo.get('ENGINE'):
        uri += dbinfo.get('ENGINE')
    if dbinfo.get('DRIVER'):
        uri += f"+{dbinfo.get('DRIVER')}"
    uri += '://'
    if dbinfo.get('USER'):
        uri += dbinfo.get('USER')
    if dbinfo.get('PASSWORD'):
        uri += f":{dbinfo.get('PASSWORD')}"
    if dbinfo.get('HOST'):
        uri += f"@{dbinfo.get('HOST')}"
    if dbinfo.get('PORT'):
        uri += f":{dbinfo.get('PORT')}"
    if dbinfo.get('DATABASE'):
        uri += f"/{dbinfo.get('DATABASE')}"
    return uri


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'scnslniuenknlnxuihce'
    DEBUG_TB_ENABLED = True
    # SESSION_TYPE = 'redis'  # 指定seesion接口
    # SESSION_REDIS = Redis(password='123')


class DevelopConfig(Config):
    DEBUG = True
    dbinfo = {
        'ENGINE': 'postgresql',
        'DRIVER': 'psycopg2',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
        'DATABASE': 'test2'
    }
    SQLALCHEMY_DATABASE_URI = get_uri(dbinfo)


class ProductConfig(Config):
    dbinfo = {
        'ENGINE': 'sqlite',
        'DRIVER': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'DATABASE': 'sqlite.db'
    }
    SQLALCHEMY_DATABASE_URI = get_uri(dbinfo)


class TESTINGConfig(Config):
    TESTING = True
    dbinfo = {
        'ENGINE': 'sqlite',
        'DRIVER': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'DATABASE': 'sqlite.db'
    }
    SQLALCHEMY_DATABASE_URI = get_uri(dbinfo)


envs = {
    'develop': DevelopConfig,
    'product': ProductConfig,
    'testing': TESTINGConfig,
    'default': DevelopConfig
}