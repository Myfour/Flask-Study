from flask_restful import Resource, abort, marshal, fields, marshal_with, reqparse  # marshal 和 marshal_with用来序列化
from flask import request
from app.models import Goods

# 这里的fields可以理解为序列化的模板
good_fields = {
    'id': fields.Integer,
    'name': fields.String(
        attribute='g_name'),  # attribute= 设置手动映射，attribute对应实际的映射到的字段
    'g_price': fields.Float,
    'url': fields.Url('single_goods', absolute=True)
}
# fields中的字段可以任意添加，但是其值不一定能获取到
single_goods_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(good_fields),  # fields.Nested可以嵌套其他fields模板
    # 'test': fields.String # 如果return的对象没有test这个key，则返回的值是null
}
# 序列化的输出结果以上面的模板里的字段为主
multi_goods_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.List(
        fields.Nested(good_fields)
    ),  # fields.List设置列表，列表如果不是一个对象可以直接使用普通的fields字段，否则还要用fields.Nested来处理对象
    'desc': fields.String(default='默认描述')  # 当这个字段没有找到映射的值时，使用default属性可以设置其默认值
}

# 使用reqparse配置可校验的输入参数
parser = reqparse.RequestParser()
parser.add_argument(
    'g_name', type=str, required=True,
    help='g_name不能为空')  # type控制参数类型，required控制是否能空，help显示当任何问题出现时的提示信息
parser.add_argument('g_price',
                    type=float,
                    required=True,
                    help='g_price不能为空或者是字符串')
# 当参数是个列表时的处理
parser.add_argument(
    'muti', dest='mu',
    action='append')  # action='append'设置结果为一个list;dest设置这个参数之后获取时使用的别名为mu

parser.add_argument('User-Agent', location='headers')
# location设置参数获取的位置，可以从header或者cookies等地方获取
# 也可以给location传入一个List来从多个地方获取，获取到多个值的情况可以通过action='append'来处理结果


class GoodsListResource(Resource):
    @marshal_with(multi_goods_fields)
    def get(self):
        goods = Goods.query.all()
        data = {
            'status': 200,
            'msg': 'Ok',
            'data': goods,
        }
        return data  # 等同于 return marshal(data,multi_goods_fields)

    @marshal_with(single_goods_fields)
    def post(self):
        # g_name = request.form.get('g_name')
        # g_price = request.form.get('g_price') # 使用request.form获取的参数无校验功能
        args = parser.parse_args()
        g_name = args.get('g_name')
        g_price = args.get('g_price')
        print(args.get('mu'))  # 当该参数设置了append的action后get到的就是一个list
        print(args.get('User-Agent'))
        goods = Goods()
        goods.g_name = g_name
        goods.g_price = g_price
        if not goods.save():
            abort(400)
        # data = {
        #     'status': 200,
        #     'msg': 'create success',
        #     'data': marshal(goods, good_fields),
        # }
        data = {
            'status': 200,
            'msg': 'create success',
            'data': goods,
            # 'test': 'haha' # 如果这个字段在fields中没有，则最后返回的结果会被忽略这个字段的内容
        }
        return data
        # return goods


class GoodsResource(Resource):
    @marshal_with(single_goods_fields)
    def get(self, id):
        goods = Goods.query.get(id)
        if not goods:
            abort(404)
        data = {
            'status': 200,
            'msg': 'ok',
            'data': goods,
        }
        return data

    def delete(self, id):
        goods = Goods.query.get(id)
        if not goods:
            abort(404)
        if not goods.delete():
            abort(400)
        data = {'status': 204, 'msg': 'delete success'}
        return data

    @marshal_with(single_goods_fields)
    def put(self, id):
        goods = Goods.query.get(id)
        if not goods:
            abort(404)
        g_name = request.form.get('g_name')
        g_price = request.form.get('g_price')
        goods.g_name = g_name
        goods.g_price = g_price
        if not goods.save():
            abort(400)
        data = {
            'status': 201,
            'msg': 'put success',
            'data': goods,
        }
        return data

    @marshal_with(single_goods_fields)
    def patch(self, id):
        goods = Goods.query.get(id)
        if not goods:
            abort(404)
        g_name = request.form.get('g_name')
        g_price = request.form.get('g_price')
        goods.g_name = g_name or goods.g_name
        goods.g_price = g_price or goods.g_price
        if not goods.save():
            abort(400)
        data = {
            'status': 201,
            'msg': 'patch success',
            'data': goods,
        }
        return data