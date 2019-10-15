from flask import Flask
from app.views.first_blue import blue
from app.views.second_blue import second
from app.views.third_blue import third
from app.views.ext import init_ext
from app.settings import config_app


def create_app():
    app = Flask(__name__)

    app.register_blueprint(blue)
    app.register_blueprint(second)
    app.register_blueprint(third)
    config_app(app)
    init_ext(app)
    return app
