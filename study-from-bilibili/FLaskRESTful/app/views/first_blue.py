# def init_route(app):
#     @app.route('/')
#     def index():
#         return '<h2>进击的巨人</h2>'

# 引入蓝图来拆分flask
from flask import Blueprint, render_template
from app.models import db, User
blue = Blueprint('blue', __name__)


@blue.route('/')
def index():
    return render_template('index.html', msg='往模板中传数据')


@blue.route('/createdb')
def createdb():
    db.create_all()
    return '创建成功'


@blue.route('/adduser')
def adduser():
    user = User(id='2', username='Tom')
    user.save()
    return '添加用户成功'


@blue.route('/dropall')
def dropall():
    db.drop_all()
    return '数据表删除成功'
