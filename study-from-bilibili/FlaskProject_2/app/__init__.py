from flask import Flask
from app.settings import Config


def create_app():
    # 初始化app
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(Config)
    # 加载扩展

    # 加载路由
    return app