from flask import Blueprint, render_template
from app.models import Student, db
import random

blue = Blueprint('blue', __name__)


def init_views(app):
    app.register_blueprint(blue)


@blue.route('/')
def index():
    return 'Index is runing'


@blue.route('/addstudent')
def add_student():
    student = Student()
    student.name = '小明' + str(random.randrange(10000))
    db.session.add(student)
    db.session.commit()
    print(db.session)
    print(type(db.session))
    return 'Add Success'


@blue.route('/addstudents')
def add_students():
    students = []
    for i in range(5):
        students.append(Student(name='小红' + str(random.randrange(10000))))

    db.session.add_all(students)
    db.session.commit()
    return 'Add_all success'


@blue.route('/getstudent')
def get_student():
    print(Student.query.first())
    print(Student.query.get(10))
    print(Student.query.get(100))  # get不到的时候返回一个None
    print(Student.query.get_or_404(100))  # get不到的时候返回一个404错误
    return 'get success'


@blue.route('/getstudents')
def get_students():

    students = Student.query.all()
    return render_template('StudentsList.html', students=students)


@blue.route('/deletestudent')
def delete_student():
    student = Student.query.first()
    db.session.delete(student)
    db.session.commit()
    return 'delete success'


@blue.route('/updatestudent')
def update_student():
    student = Student.query.first()
    student.name = 'Jomndnn'
    db.session.add(student)
    db.session.commit()
    return 'update success'