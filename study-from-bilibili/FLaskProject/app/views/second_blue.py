from flask import Blueprint

second = Blueprint('second', __name__)


@second.route('/second')
def index():
    return 'This page from second BluePrint ‘blue’'