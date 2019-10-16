from flask import Flask
from app.views import init_view
from app.ext import init_ext
from app.settings import envs


def create_app():
    app = Flask(__name__)
    app.config.from_object(envs.get('testing'))
    init_ext(app)
    init_view(app)
    return app
