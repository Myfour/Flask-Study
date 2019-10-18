from flask import Blueprint, redirect, url_for, request, Response, render_template, abort, session
# from app.ext import db
from app.models import db
# 上面这里出了一个BUG如果不导入models中的db对象，则flask中目前就没有连接models.py文件，也就看不到模型的代码
# 使用上面ext中的db对象也是可以的，不过需要在额外将models.py导入，才能正确使用model

blue = Blueprint('blue', __name__)


def init_view(app):
    app.register_blueprint(blue)


@blue.route('/')
def test():
    return 'test'


@blue.route('/user/<id>')
def user(id):
    print(id)
    print(type(id))
    return 'User API'


# 一个方法可以对应多个路由
@blue.route('/users/<int:id>')
@blue.route('/userstr/<string:id>')
def users(id):
    print(id)
    print(type(id))
    return 'Users API'


@blue.route('/getpath/<path:address>')
def getpath(address):
    print(address)
    print(type(address))
    return 'getAdress'


@blue.route('/getuuid/<uuid:uu>/')
def getuuid(uu):
    print(uu)
    print(type(uu))
    return 'getUUID'


@blue.route('/redirect')
def red():
    # redirect实现重定向
    # return redirect('/')
    # url_for路由的反向解析，函数名为蓝图名.函数名，配合redirect使用
    # return redirect(url_for('blue.test'))
    # 为url_for传参
    return redirect(url_for('blue.getpath', address='skjef/dlsef/sef'))


@blue.route('/getrequest', methods=['GET', 'POST', 'PUT', 'DELETE'])
def getrequest():
    print(request.host)
    print(request.url)
    if request.method == 'GET':
        return f'GET SUCCESS {request.remote_addr}'
    elif request.method == 'POST':
        return 'POST SUCCESS'
    else:
        return f'{request.method} is not support'


@blue.route('/createdb')
def createdb():
    db.create_all()
    return '数据库创建成功'


@blue.route('/sendrequest', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def sendrequest():
    print(request.args)
    print(type(request.args))
    print(request.form)
    print(type(request.form))
    print(request.headers)
    print(type(request.headers))
    return 'send success'


@blue.route('/getresponse')
def getresponse():
    # return 'Hello',400

    # result = render_template('index.html')  # render_template就是把模板变成字符串
    # print(result)
    # print(type(result))

    # 主动抛出错误请求
    abort(401)
    return


# 捕获错误请求，可以用来捕获401请求
@blue.errorhandler(401)
def error_401(error):
    print(error)
    print(type(error))
    return Response('What 401 happen', 401)


@blue.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        response = Response(f'登录成功 ^-^ => {username}')
        # response.set_cookie('username', username) # 设置cookie存储
        session[
            'username'] = username  # flask的session在cookie中序列化了一个session的key-value
        session['password'] = username  # 会自动组合所有session为一个key-value
        return response


@blue.route('/mine')
def mine():
    # username = request.cookies.get('username')  # 获取cookie存储
    username = session.get('username')
    print(session)
    print(type(session))
    if username:
        return render_template('mine.html', username=username)
    else:
        abort(401)


@blue.route('/students')
def students():
    studnet_list = [i for i in range(10)]
    return render_template('students.html', student_list=studnet_list)


@blue.route('/register')
def register():
    return render_template('user/user_register.html', title='用户登录注册')


@blue.route('/register2')
def register2():
    return render_template('user/user_register2.html', title='用户登录注册2')


@blue.route('/bootstrap')
def bootstrap():
    return render_template('base.html')