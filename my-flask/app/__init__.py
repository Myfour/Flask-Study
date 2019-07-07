from flask import Flask
from .views import bp
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Fuxk you'
    bootstrap.init_app(app)

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    app.register_blueprint(bp)
    return app