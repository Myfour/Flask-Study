from flask import Blueprint, render_template, g, request, render_template, redirect, flash, url_for
from app.models import News, db, Students
import random
from werkzeug.security import generate_password_hash, check_password_hash
blue = Blueprint('blue', __name__)
from flask_mail import Message
from app.ext import mail


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
        username = request.form.get('username')
        password = request.form.get('password')
        students = Students()
        students.s_name = username
        students.password = password
        db.session.add(students)
        db.session.commit()
        return 'Register Success'


@blue.route('/student/login', methods=['POST', 'GET'])
def student_login():
    if request.method == 'GET':
        return render_template('StudentLogin.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        student = Students.query.filter_by(s_name=username).first()
        if student:
            if student.check_password(password):
                return 'login Success'
            else:
                flash('Password not right')
                return redirect(url_for('blue.student_login'))
        else:
            flash('User not exist')
            return redirect(url_for('blue.student_login'))


@blue.route('/sendmail')
def send_mail():
    msg = Message('Flask Email', recipients=['oz_myx@126.com'])
    msg.body = '哈哈 不过如此'
    msg.html = '<h1>你他娘的可真是个天才</h1>'
    mail.send(message=msg)
    return 'Send success'