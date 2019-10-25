from flask_restful import Api
from app.apis.userlist_api import HelloResource

api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(HelloResource, '/hello')
