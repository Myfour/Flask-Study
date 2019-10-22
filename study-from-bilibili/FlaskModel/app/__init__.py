from flask import Flask
from app.ext import init_ext
from app.views import init_views
from app.settings import envs
from app import models


def create_app():
    app = Flask(__name__,
                template_folder='../templates')  # Flask实例中可以设置默认模板的寻找路径
    init_ext(app)
    init_views(app)
    app.config.from_object(envs['develop'])
    return app
