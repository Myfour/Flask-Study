from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


# 这里蓝图的配置个人认为不太好，应该有更好的方式
def init_bp(app):
    from app.main import main
    app.register_blueprint(main)


def init_ext(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])
    init_ext(app)
    init_bp(app)
    return app