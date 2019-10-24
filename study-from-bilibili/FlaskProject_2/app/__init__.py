from flask import Flask
from app.ext import init_ext
from app.views import init_view
from app.settings import envs
from app.middleware import load_middleware
from app import models


def create_app():
    app = Flask(__name__)
    app.config.from_object(envs['develop'])  # 注意配置读取的顺序，一定要在配置扩展等东西前面
    init_ext(app)
    init_view(app)
    load_middleware(app)
    return app
