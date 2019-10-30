from . import main
from flask import render_template, abort, request, redirect, session, url_for, flash
from .forms import NameForm
from app.models import User, db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        if session.get('name') != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('form_test.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


@main.route('/test')
def test():
    # return request.cookies
    # return request.endpoint, 400
    # print(url_for('main.test', _external=True))
    # return render_template('base.html')
    # return render_template('500.html')
    # abort(500)
    return render_template('test.txt')  # render_template可以读取文本文件作为模板


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@main.app_errorhandler(500)
def internal_error(e):
    return render_template('500.html')