from flask import Blueprint

blue = Blueprint('blue', __name__)


@blue.route('/')
def index():
    return 'Index Page'