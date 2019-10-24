from app.views.HelloView import blue


def init_view(app):
    app.register_blueprint(blue)
