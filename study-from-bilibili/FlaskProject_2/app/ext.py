from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()
mail = Mail()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    toolbar.init_app(app)
    mail.init_app(app)