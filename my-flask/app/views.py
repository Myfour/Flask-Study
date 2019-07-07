from flask import Blueprint, request, render_template, current_app
from .forms import NameForm

bp = Blueprint('auth', __name__)


@bp.route('/')
def index():
    return f'This is BP index.... and request is {request.method}'


@bp.route('/test')
def test():
    return render_template('test.html', name='MYFour')


@bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        return f'My Name Is {request.form.get("name")}'
    return render_template('form.html', form=NameForm())


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', app=current_app), 404


@bp.app_errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500
