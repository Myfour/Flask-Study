from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from ..models import User
from app import db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
        # 在蓝图中url_for的用法略有不同，蓝图中默认在url_for中的端点名前加上命名空间名.
        # 如果是在当前蓝图汇总操作的话可以简写为.不加命名空间名，但是如果要跨蓝图就要使用命名空间.端点名了
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())
