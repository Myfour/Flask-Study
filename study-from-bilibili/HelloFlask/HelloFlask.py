from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
db = SQLAlchemy()
db.init_app(app)
app.debug = True
app.config['SECRET_KEY'] = 'sdfsdfwesw'
DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create')
def create():
    db.create_all()
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)
