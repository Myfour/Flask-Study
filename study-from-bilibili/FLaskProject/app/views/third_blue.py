from flask import Blueprint

third = Blueprint('third', __name__)


@third.route('/third')
def index():
    return 'This page from third BluePrint ‘blue’'