from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm  # forms不是一个文件夹 是一个文件 所以from的时候要加一个.


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Myfour'}
    posts = [  # fake array of posts
        {
            'author': {
                'nickname': 'John'
            },
            'body': 'Beautiful day in Portland!'
        }, {
            'author': {
                'nickname': 'Susan'
            },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template(
        'index.html',
        title='Myfour',
        user=user,
        posts=posts,
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f'Login requested for OpenID="{form.openid.data}",remember_me={str(form.remember_me.data)}'
        )  # flash用于向下次request闪现数据，需要在模板中使用get_flashed_messages()函数获取内容
        return redirect('/index')
    print(form.openid.errors)
    return render_template('login.html', title='Sign in', form=form)
