from app import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # lazy='dynamic'的意义在于默认当使用Role对象的users属性时会直接调用all()返回查询到的结果集
    # 如果想在users的基础上使用其他过滤器就需要lazy='dynamic'属性，可以使users属性获取到的对象也是
    # 类似BaseQuery的一个对象

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f'<User {self.username}>'
