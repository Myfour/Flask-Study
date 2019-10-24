from app.ext import db


class News(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True)  # 个人理解加了primary_key=True以后就自带了autoincrement=True了
    n_title = db.Column(db.String(32))
    n_content = db.Column(db.String(256))


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(16), unique=True)
    s_password = db.Column(db.String(256))
