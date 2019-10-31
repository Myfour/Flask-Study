from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


# 这里蓝图的配置个人认为不太好，应该有更好的方式
def init_bp(app):
    from app.main import main
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')


def init_ext(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])
    init_ext(app)
    init_bp(app)
    return app