# 启动测试用的服务器
# 1.设置环境变量,set FLASK_APP=xxxx.py
# 2.启动 flask run
# 3.如需热加载和调试模式 set FLASK_DEBUG=1；然后重启服务器
from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/')  # URL映射
def hello_world():
    return 'Hello Flask ..'


@app.route('/other')
def other():
    return 'This is other page !!!!!'


# URL变量替换
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'


# URL变量的类型转换
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {subpath}'


# url末尾加/的影响
@app.route('/test/')
def test():
    return 'This is / test....'


# 命令行运行 python hello.py
# url_for 函数可以根据方法名和传入的参数生成一个url；url_for() 函数用于构建指定函数的 URL
with app.test_request_context():
    print(url_for('hello_world'))
    print(url_for('other'))
    print(url_for('other', next='999'))
    print(url_for('show_user_profile', username='Kaisi'))
    print(url_for('static', filename='Nes.css'))

# HTTP Method


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Now Do the POST............'
    else:
        return 'Now Do the GET............ '


# 模板渲染
@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
