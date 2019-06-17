from flask import (Flask, request, make_response, redirect, abort,
                   render_template, url_for)

# 导入Flask的扩展
from flask_bootstrap import Bootstrap  # 导入扩展通常通过 import flask_xxxxxx 其中xxxxx为扩展的名称

print(__name__)
app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')  # 设置func到url的路由
def index():  # index()这样的函数称为视图函数
    return '<h1 style="color:green" align="center">Hello Dog Book ! </h1>'  # 视图函数return的东西称为响应


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


if __name__ == '__main__':
    app.run(debug=True)  # debug=True设置调试方式启动,命令含中需设置FLASK_DUBUG=1启动调试
    # 启动Flask应用可以使用代码和命令两种方式启动
    # 命令行模式需要设置环境变量FLASK_APP=应用的文件或包
    # 使用代码启动则不需要，一般用于单元测试
