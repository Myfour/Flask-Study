from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
session = Session()  # session咋redis中的默认生命周期为31天
bootstrap = Bootstrap()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)
    bootstrap.init_app(app)