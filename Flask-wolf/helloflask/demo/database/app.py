from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_sqlalchemy import SQLAlchemy
from forms import NewNoteForm, EditNoteForm, DeleteNoteForm
from flask_migrate import Migrate
import os
import click

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'guess'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def __repr__(self):
        return f'<Note {self.body}>'


'''
自定义一个更新数据库表的命令
'''
@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


'''
数据查询：
Note.query.all()
Note.query.get()
Note.query.first()
Note.query.count()
等等.......

数据过滤:
filter()

filter中的等于与不等于：
Note.query.filter(Note.body=='SHAVE')
Note.query.filter(Note.body!='SHAVE')

# 直接打印filter()得到的对象可以查看SQL语句

filter中其他判断不同上述两个：
    like语句:
    Note.query.filter(Note.body.like('%foo%'))

    in语句：
    Note.query.filter(Note.body.in_(['foo','bar','baz']))

    not-in:
    Note.query.filter(~Note.body.in_(['foo', 'bar', 'baz']))

    .....

其实filter_by更易用：

    Note.query.filter_by(body='SHAVE')


更新：
直接赋值给一个已有对象的属性，最后再commit,此时不必add了
只有要插入新的记录或要将现有的记录添加到会话中时才需要使用
add（）方法，单纯要更新现有的记录时只需要直接为属性赋新值，然
后提交会话。

删除记录：
note=Note.query.get(2)
db.session.delete(note)
db.session.commit()
'''
@app.route('/new', methods=['GET', 'POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved!')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)


@app.route('/')
def index():
    notes = Note.query.all()
    form = DeleteNoteForm()
    return render_template('index.html', notes=notes, form=form)


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('Your note is updated.')
        return redirect(url_for('index'))
    form.body.data = note.body  # 反过来通过数据库内容来显示表单中的数据
    return render_template('edit_note.html', form=form)


'''
在页面中处理删除操作时，不建议直接制造一个GET请求的连接来删除，不安全
需要单独生成一个Delete的Form来处理删除操作
'''
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is deleted.')
    else:
        abort(400)
    return redirect(url_for('index'))


'''
注册shell的上下文
'''
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Note)


'''
模型关系
一对多关系：
    1.先建立外键，外键只能表示单一值，所以只能在多的一端
    2.定义关系属性，定义在一这一端
    3. 建立关系：
        创建对象，在一端创建对象时，给关系属性append()上多端的对象；
        通过给外键字段赋值；
        两种方式，推荐第一种
多对一关系:
    而不是一端的list属性
    基本同上，只是将关系属性定义在多端，此时这个关系属性为标量属性，
'''


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    phone = db.Column(db.String(20))
    articles = db.relationship('Article')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(
        db.Integer, db.ForeignKey('author.id')
    )  # 为什么是author.id 因为 这里填的内容为 (表名.字段名) ;表名为小写的author而不是大写的类名

    def __repr__(self):
        return f'<Article {self.body}>'


'''
定义双向关系：
    1.使用两个relationship来定义
        添加关系两端都可以，如果在标量端也就是多端，
        给writer关系属性赋值对象就行了，如果要取消关系就赋值writer为空就行了
    2.使用backref来简化定义
'''


class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    books = db.relationship('Book', back_populates='writer')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    writer = db.relationship('Writer', back_populates='books')


class Singer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    songs = db.relationship('Song', backref='singer')
    # 因为是在一端设置的关系，如果想设置另一端的关系的一些参数则需要使用
    # backref函数
    # relationship('Song', backref=backref('singer', uselist=False))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    singer_id = db.Column(db.Integer, db.ForeignKey('singer.id'))


'''
一对一关系：
    在一对多关系上建立，需要把关系属性不是标量属性的一端改为标量属性，通过
    uselist=False来实现
'''


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    capital = db.relationship('Capital', uselist=False)


class Capital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country')


'''
多对多关系
'''
association_table = db.Table(
    'association',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    grade = db.Column(db.String(20))
    teachers = db.relationship('Teacher',
                               secondary=association_table,
                               back_populates='students')


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    office = db.Column(db.String(20))
    students = db.relationship('Student',
                               secondary=association_table,
                               back_populates='teachers')
