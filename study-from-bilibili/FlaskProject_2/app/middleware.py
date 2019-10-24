from flask import current_app, g


def load_middleware(app):
    @app.before_request
    def before():
        print('发起请求前执行......')
        # print(current_app.config)
        g.msg = '哈哈'  # g对象实现跨函数传递数据

    @app.after_request
    def after(resp):
        print('请求结束执行......')
        print(resp)
        print(type(resp))
        return resp