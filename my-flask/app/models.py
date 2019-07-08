from . import db


class Person(db.Model):
    __tablename__ = '人'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
