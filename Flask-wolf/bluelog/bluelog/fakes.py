from bluelog.models import Admin, Category, Post, Comment
from bluelog.extensions import db
from faker import Faker
from sqlalchemy.exc import IntegrityError
import random
fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='Bluelog',
        blog_sub_title="No,i'm the real thing",
        name='Mima Kirigoe',
        about='Um,I,Mima Kirigoe, had a fun time as a member od CHAM...')
    admin.set_password('hello world')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(title=fake.sentence(),
                    body=fake.text(2000),
                    category=Category.query.get(
                        random.randint(1, Category.query.count())),
                    timestamp=fake.date_time_this_year())
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(author=fake.name(),
                          email=fake.email(),
                          site=fake.url(),
                          body=fake.sentence(),
                          timestamp=fake.date_time_this_year(),reviewd=True,post=,)
