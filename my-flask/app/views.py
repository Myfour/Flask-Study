from flask import Blueprint, request, render_template, current_app, redirect, url_for, session, flash
from .forms import NameForm
# from app import db

bp = Blueprint('auth', __name__)


@bp.route('/')
def index():
    return f'This is BP index.... and request is {request.method}'


@bp.route('/test')
def test():
    return render_template('test.html', name='MYFour')


@bp.route('/form', methods=['GET', 'POST'])
def form():
    forms = NameForm()
    if request.method == 'POST':
        session['name'] = forms.name.data
        flash(session.get('name'))
        return redirect(url_for('.form'))
    return render_template('form.html', form=forms, name=session.get('name'))


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', app=current_app), 404


@bp.app_errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


@bp.route('/db')
def db_create():
    from . import db
    try:
        db.create_all()
        flash('数据库创建的成功')
    except Exception as e:
        flash(f'数据库创建出现异常,{e}')

    return redirect(url_for('.form'))