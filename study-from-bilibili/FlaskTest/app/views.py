from flask import Blueprint
from app.models import db
blue = Blueprint('blue', __name__)


def init_blueprint(app):
    app.register_blueprint(blue)


@blue.route('/')
def index():
    return 'Index'


@blue.route('/create')
def create():
    db.create_all()
    return 'Success'