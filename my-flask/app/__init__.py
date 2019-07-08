from flask import Flask
from .views import bp
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.dirname(__file__)

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Fuxk you'
    bootstrap.init_app(app)

    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir,"data.sqlite")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    app.register_blueprint(bp)
    return app