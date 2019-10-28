from flask_restful import Resource, abort, marshal, fields, marshal_with  # marshal 和 marshal_with用来序列化
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
        g_name = request.form.get('g_name')
        g_price = request.form.get('g_price')
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