from flask import Flask
from app.settings import envs
from app.ext import init_ext
from app.views import init_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(envs['testing'])
    init_ext(app)
    init_blueprint(app)
    return app