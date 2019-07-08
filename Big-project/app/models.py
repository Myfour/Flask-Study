from . import db


# 模型
class Role(db.Model):
    __tablename__ = 'roles'  # 定义生成的数据库的名称
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 显示相关的多 的一端的内容；backref用来设置从多的一端用什么来获取一这一端；当模型中有多个相同模型的关系时
    # 必须设置backref来确定反向获取用的是哪个模型
    # lazy参数有妙用 dynamic值 修改了关系字段的默认行为中隐式调用的all()，使我们可以在关系字段中添加过滤器使用
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 对应的外键

    def __repr__(self):
        return f'<User {self.username}>'