from flask import Flask, render_template
from bluelog.settings import config
import os
from bluelog.extensions import bootstrap, ckeditor, db, mail, moment
# from bluelog.blueprints.auth import auth_bp
'''
Flask的自动发现程序实例机制还
包含另一种行为：Flask会自动从环境变量FLASK_APP的值定义的模块
中寻找名为create_app（）或make_app（）的工厂函数，自动调用工厂
函数创建程序实例并运行
'''


def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_logging(app)
    register_shell_context(app)
    register_template_context(app)

    print(app.config)
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    # app.register_blueprint(blog)
    # app.register_blueprint(admin, url_prefix='/admin')
    # app.register_blueprint(auth, url_prefix='/auth')
    pass


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass


def register_logging(app):
    pass  # 第14章会详细介绍日志


def register_commands(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400
