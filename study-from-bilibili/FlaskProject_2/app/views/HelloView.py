from flask import Blueprint, render_template, g, request, render_template
from app.models import News, db
import random
blue = Blueprint('blue', __name__)


@blue.route('/')
def index():
    return 'Index Page'


@blue.route('/addnews')
def add_news():
    news = News()
    news.n_title = f'周润发{random.randrange(1000)}'
    news.n_content = f'福利捐款{random.randrange(1000)}w'
    db.session.add(news)
    db.session.commit()
    return 'add success'


@blue.route('/getnews')
def get_news():
    news = News.query.all()
    print(g.msg)
    return render_template('NewsList.html', news=news)


'''
flask 
四大内置对象：
session
request
g
config
'''
@blue.route('/student/register', methods=['POST', 'GET'])
def student_register():
    if request.method == 'GET':
        return render_template('StudentRegister.html')
    elif request.method == 'POST':
        print(request.data.get('username'))
        print(request.form)
        return ''