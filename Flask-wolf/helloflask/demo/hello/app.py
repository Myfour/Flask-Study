from flask import Flask
import click
app = Flask(__name__)


# 多个路由可以绑定到同一个视图函数上
@app.route('/hi')
@app.route('/hello')
def index():
    return '<h1>Hello , Flask !</h1>'


@app.route('/greet/<name>')
@app.route('/greet')
def greet(name='Programmer'):
    return f'<h1>Hello , {name}</h1>'


'''
You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.
启动服务时自动寻找wsgi或者app为名的模块，如果没设置FLASK_APP环境变量的话


自动发现程序实例机制：
·从当前目录寻找app.py和wsgi.py模块，并从中寻找名为app或 application的程序实例。
·从环境变量FLASK_APP对应的值寻找名为app或application的程序 实例。
·Flask的自动发现程序实例机制还有第三条规则：如果安装了 python-dotenv，那么在使用flask run或其他命令时会使用它自动 从.flaskenv文件和.env文件中加载环境变量。


最好在程序实例app创建后就 加载配置
'''
@app.cli.command('say-hello')
def hello():
    '''
    Just Say Hello
    '''
    click.echo('Hello , Human !')