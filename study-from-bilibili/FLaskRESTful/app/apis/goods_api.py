from flask_restful import Resource, abort, marshal, fields, marshal_with
from flask import request
from app.models import Goods

# 这里的fields可以理解为序列化的模板
good_fields = {
    'g_name': fields.String,
    'g_price': fields.Float,
}
# fields中的字段可以任意添加，但是其值不一定能获取到
single_goods_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(good_fields),  # fields.Nested可以嵌套其他fields模板
    # 'test': fields.String # 如果return的对象没有test这个key，则返回的值是null
}


class GoodsListResource(Resource):
    def get(self):
        pass

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
