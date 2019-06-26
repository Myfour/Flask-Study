from flask import (Flask, request, make_response, redirect, abort,
                   render_template, url_for, session, flash)
from datetime import datetime
# 导入Flask的扩展
from flask_bootstrap import Bootstrap  # 导入扩展通常通过 import flask_xxxxxx 其中xxxxx为扩展的名称
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_mail import Message

from threading import Thread
import os

# app文件的根目录
basedir = os.path.abspath(os.path.dirname(__file__))

print(__name__)
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
# 配置邮件
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
# 配置用来发邮件的邮箱账号
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get(
    'MAIL_PASSWORD')  # eucilwvlrztrbajc
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <913906842@qq.com>'  # 发送方
mail = Mail(app)
# 配置SQLAlchemy
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir,"data.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # 获取SQLAlchemy实例对象

# 配置迁移
migrate = Migrate(app, db)
'''
执行命令 flask db init 添加迁移的支持，该命令创建相应的migrations文件夹
生成迁移脚本 flask db migrate 自动创建一个迁移的脚本
应用迁移 flask db upgrade
'''

# 操作模型
'''
db.create_all() 创建所有的数据库表,已存在的表执行了不会重新创建
db.drop_all() 删除所有数据库表

# 创建一个Role对象
admin_role=Role(name='Admin') 
# 创建User对象，其中role属性来自于关系字段的backref属性
user_john=User(username='john',role=admin_role) 
# 此时只是单独创建了对象 还未提交到数据库，需要利用数据库的session来提交,这个session也称为事务
# 先添加到session中，再提交
db.session.add(admin_role) 
db.session.add_all([admin_role,user_john])
db.session.commit()

# session.add可以更新数据
admin_role.name='Administrator'
db.session.add(admin_role)
db.session.commit()

# 删除数据
db.session.delete(mod_role)
db.session.commit()

# 查询数据
Role.query.all()
User.query.all()
# query对象可以配置过滤器 来过滤查询结果
User.query.filter_by(role=user_role).all()
# query对象对应的sql语句可以通过str()转换query对象为str来查看
str(User.query.filter_by(role=user_role))
# all() first() all获取结果为一个list,如果确定结果只有一个可以用first()来直接获取该对象

# 一对多关系查询
users=user_role.users
users结果会隐式调用all(),以至于我们无法在users的基础上添加过滤器,通过给模型的relationship
字段添加lazy参数来改变这个默认行为。
'''


# 模型
class Role(db.Model):
    __tablename__ = 'roles'  # 定义生成的数据库的名称
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 显示相关的多 的一端的内容；backref用来设置从多的一端用什么来获取一这一端；当模型中有多个相同模型的关系时
    # 必须设置backref来确定反向获取用的是哪个模型
    # lazy参数有妙用 dynamic值 修改了关系字段的默认行为中隐式调用的all()，使我们可以在关系字段中添加过滤器使用
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 对应的外键

    def __repr__(self):
        return f'<User {self.username}>'


app.config['SECRET_KEY'] = 'hard to guess string'

# 管理员邮箱，来自环境变量
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')


@app.route('/', methods=['GET', 'POST']
           )  # 设置func到url的路由;methods参数的设置是为了该视图可以处理POST的请求，否则只可以处理GET
# 最后别让POST请求成为最后一个请求
def index():  # index()这样的函数称为视图函数
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            print('New User...')
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                print('Ready to send email...')
                send_email(app.config['FLASKY_ADMIN'],
                           'New User',
                           'mail/new_user',
                           user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        # if old_name and old_name != form.name.data:
        #     flash('Looks like you have changed your name!')  # 存在其中的消息只闪现显示一次
        # session['name'] = form.name.data
        # print(session)
        return redirect(url_for('index'))  # url_for函数第一个参数是端点名

    # print(session)
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))
    # 视图函数return的东西称为响应


# 原始的配置路由的方法 不使用装饰器，其实装饰器的本质也是调用这个方法
def index2():
    return '<h1 style="color:red" align="center">Hello Dog Book ! </h1>'


app.add_url_rule('/index2', 'index2',
                 index2)  # 配置路由的原始方法，@app.route 装饰器其实也是调用这个函数来实现的


@app.route('/user/<name>')  # 动态路由,<>内的内容就是动态的参数，该参数会传给视图函数
def user(name):
    # 视图函数return的东西称为响应
    return render_template('user.html',
                           name=name)  # 渲染模板，默认从根目录下的templates文件夹下寻找模板


# 请求对象request
@app.route('/requests')
def request_use():
    user_agent = request.headers.get('User-Agent')
    # request.form # 获取所提交的表单数据
    # request.args  # 获取URL查询字符串中的数据
    return f'<p>Your browser is <b style="color:blue">{user_agent}</b></p>'


# 响应
@app.route('/response1')
def response_test():
    return '<h1>Somethinggggggg Nottttt Founddddd!!!!!!!!!!</h1>', 404
    # 可以通过在return的结果元组中加入状态码来控制响应的状态


@app.route('/response2')
def response_test2():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


# 重定向
@app.route('/other')
def other():
    # return redirect('/requests')
    return redirect('https://www.baidu.com')


# abort异常响应
@app.route('/abort')
def abort_test():
    abort(400)


# 自定义错误页面
# 使用app.errorhandler装饰器
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('505.html'), 505


# 动态生成URL链接
# url_for函数 根据构建路由的endpoint名来构建路由，可以传入一些静态与动态的参数，以及显示绝对路径
@app.route('/show_url')
def show_url():
    return f'''<h1>{url_for('index')}</h1>
               <br>
               <h1>{url_for('index',_external=True)}</h1>
               <br>
               <h1>{url_for('user',name='Lee')}</h1>
               <br>
               <h1>{url_for('user',name='Lee',_external=True)}</h1>
               '''


# moment test
@app.route('/moment_test')
def moment_test():
    return render_template('index.html', current_time=datetime.utcnow())


# 定义表单类
class NameForm(FlaskForm):
    name = StringField('What is your name?', [DataRequired()])
    submit = SubmitField('Submit')


# 每次启动flask shell 需要重新导入所需的包
# 是flask shell 自动导入所需的内容


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
    # dict中的这几个变量以及app被自动导入到flask shell环境中


# 邮件
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True)  # debug=True设置调试方式启动,命令含中需设置FLASK_DUBUG=1启动调试
    # 启动Flask应用可以使用代码和命令两种方式启动
    # 命令行模式需要设置环境变量FLASK_APP=应用的文件或包
    # 使用代码启动则不需要，一般用于单元测试
