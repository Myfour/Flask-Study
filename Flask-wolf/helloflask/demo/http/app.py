from jinja2.utils import generate_lorem_ipsum
from flask import Flask, request, abort, make_response, jsonify, redirect, url_for, session
import os
from urllib.parse import urlparse, urljoin
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey')


@app.route('/hello')
def hello():
    name = request.args.get('name')
    if not name:
        name = request.cookies.get('name', 'Human')
    response = f'<h1>Hello , {name}</h1>'
    if session.get('logged_in'):
        response += ' has [Authenticated]'
    else:
        response += ' not [Authenticated]'
    return response


@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'


@app.route('/404')
def not_found():
    abort(404)


@app.route('/hello-201')
def hello_201():
    return 'Hello', 201


# plain纯文本输出结果就不会解析html标签了
@app.route('/foo')
def foo():
    response = make_response('<h1>Hello_Worlds--..--~1</h1>')
    response.mimetype = 'text/plain'
    # response.mimetype = 'text/html'
    return response


@app.route('/getjson')
def getjson():
    return jsonify(name='Splatoon', price='$250'), 500  # 默认状态码为200,可以手动修改


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/dosomething')
def dosomething():
    # return redirect(request.referrer or url_for('hello'))
    return redirect_back()


@app.route('/one')
def one():
    return f'<h1>One Page</h1><a href={url_for("dosomething",next=request.full_path)}>Do SomeThing</a>'


@app.route('/two')
def two():
    return f'<h1>Two Page</h1><a href={url_for("dosomething",next=request.full_path)}>Do SomeThing</a>'


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


'''
重定向时存在
开放重定向漏洞，需要防止有人利用重定向，通过url传入重定向的连接，来把用户导入一个其他网址
所以需要下面的函数来判断重定向的地址与原始网站是否是同一个主机
'''


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    ref_url = urlparse(urljoin(request.host_url, target))
    print(host_url, ref_url)
    return ref_url.scheme in ('http',
                              'https') and host_url.netloc == ref_url.netloc


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)  # 生成两段随机文本
    return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function() {
    $('#load').click(function() {
    $.ajax({
    url: '/more', // 目标URL
    type: 'get', // 请求方法
    success: function(data){ // 返回2XX响应后触发的回调函数
    $('.body').append(data); // 将返回的响应插入到页面中
    }
    })
    })
    })
    </script>''' % post_body


@app.route('/more')
def more():
    post_body = generate_lorem_ipsum(n=1)
    return post_body


'''
实现服务器端推送的一系列技术被合称为HTTP Server Push（HTTP
服务器端推送）

- 传统轮询
- 长轮询
- Server-sent Events (SSE)

全双工通信 websocket
'''