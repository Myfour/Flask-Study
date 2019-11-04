from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import NewNoteForm
import os
import click

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'guess'

db = SQLAlchemy(app)


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
    return render_template('index.html', notes=notes)
