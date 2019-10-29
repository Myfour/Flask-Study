import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # or实现了if else 的赋值
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # 使用字典的get实现类似上面or赋值的效果
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL',
                                  'true').lower() in ['true', 'on', 1]
    MAIL_USERNAME = '913906842@qq.com'
    MAIL_PASSWORD = 'uqbugwipehjybced'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = MAIL_USERNAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL'
    ) or f"sqlite:///{os.path.join(BASE_DIR, 'data-dev.sqlite')}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL'
    ) or f"sqlite:///{os.path.join(BASE_DIR, 'data-test.sqlite')}"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, 'data.sqlite')}"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
