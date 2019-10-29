from . import main
from flask import render_template, abort


@main.route('/')
def index():
    return 'RUN OK'
