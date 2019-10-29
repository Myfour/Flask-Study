from flask import Flask
from config import config
from app.main import main


def init_bp(app):
    app.register_blueprint(main)


def init_ext(app):
    pass


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])
    init_ext(app)
    init_bp(app)
    return app