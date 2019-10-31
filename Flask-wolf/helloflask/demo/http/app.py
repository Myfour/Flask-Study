from flask import Flask, request, abort
app = Flask(__name__)


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')
    return f'<h1>Hello , {name}</h1>'


@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'


@app.route('/404')
def not_found():
    abort(404)