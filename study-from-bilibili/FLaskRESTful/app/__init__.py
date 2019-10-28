from flask import Flask
from app.ext import init_ext
from app.settings import envs
from app.views import init_views
from app.apis import init_api
from app import models


def create_app():
    app = Flask(__name__)
    app.config.from_object(envs.get('develop'))
    init_ext(app)
    init_views(app)
    init_api(app)
    return app
