from flask_restful import Api
from app.apis.userlist_api import HelloResource
from app.apis.goods_api import GoodsListResource

api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(HelloResource, '/hello')
api.add_resource(GoodsListResource, '/goods')
