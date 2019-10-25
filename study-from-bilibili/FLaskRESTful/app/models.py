from app.views.ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))

    def save(self):
        db.session.add(self)
        db.session.commit()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(20))
    s_password = db.Column(db.String(256))


print('models.py is run')