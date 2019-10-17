from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


@app.route('/')
def index():
    return '<h1>Hello Flask</h1>'


@app.route('/create')
def create():
    db.create_all()
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)
