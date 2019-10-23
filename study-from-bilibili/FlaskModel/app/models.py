from app.ext import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))


class User(db.Model):
    __tablename__ = 'UserModel'  # 手动设置orm生成的表的名称
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(16), unique=True)
    u_des = db.Column(db.String(128), nullable=True)


class Animal(db.Model
             ):  # flask的模型继承后默认都在一张表里，造成了数据的混乱，通过添加__abstract__抽象来控制继承对象生成表
    # 抽象的模型不会在数据库中生成
    __abstract__ = True  # 没设置该属性，就只会生成animal表，其中包含了dog和cat的属性
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_name = db.Column(db.String(16))


class Dog(Animal):
    d_legs = db.Column(db.Integer, default=4)


class Cat(Animal):
    c_eat = db.Column(db.String(32), default='fish')


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(16))


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_position = db.Column(db.String(16))
    a_customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
