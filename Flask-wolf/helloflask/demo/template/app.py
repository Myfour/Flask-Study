from flask import Flask, render_template, flash, redirect, url_for
app = Flask(__name__)
user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {
        'name': 'My Neighbor Totoro',
        'year': '1988'
    },
    {
        'name': 'Three Colours trilogy',
        'year': '1993'
    },
    {
        'name': 'Forrest Gump',
        'year': '1994'
    },
    {
        'name': 'Perfect Blue',
        'year': '1997'
    },
    {
        'name': 'The Matrix',
        'year': '1999'
    },
    {
        'name': 'Memento',
        'year': '2000'
    },
    {
        'name': 'The Bucket list',
        'year': '2007'
    },
    {
        'name': 'Black Swan',
        'year': '2010'
    },
    {
        'name': 'Gone Girl',
        'year': '2014'
    },
    {
        'name': 'CoCo',
        'year': '2017'
    },
]


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


# 自定义上下文变量，通过该装饰器添加变量或者函数到上下文中
@app.context_processor
def foo():
    return {'foo': 'Your are fool!', 'test': lambda: 'this is test function'}


# 往上下文中添加模板的全局函数
@app.template_global()
def bar():
    return 'I am bar global function'


# render_template 就是将模板返回一个对应的字符串 ，最后交给return返回这个模板的字符串表示
@app.route('/index')
def index():
    # print(type(render_template('test.html')))
    # print(render_template('test.html'))
    return 'index'


@app.route('/flash')
def just_flash():
    flash("i'm flash who is looking for me?")
    return redirect(url_for('watchlist'))


app.secret_key = 'guess'
