from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    toolbar.init_app(app)
