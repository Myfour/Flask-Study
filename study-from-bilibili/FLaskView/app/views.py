from flask import Blueprint, redirect, url_for, request
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