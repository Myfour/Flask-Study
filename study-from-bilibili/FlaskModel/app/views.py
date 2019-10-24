import random

from flask import Blueprint, render_template, request

from app.models import Cat, Dog, Student, db, Customer, Address

blue = Blueprint('blue',
                 __name__,
                 template_folder='../templates',
                 url_prefix='/db')  # 也可以在蓝图中设置模板路径,以及路由前缀


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


@blue.route('/addcat')
def add_cat():
    cat = Cat()
    cat.a_name = '加菲猫'
    cat.c_eat = '骨头'
    db.session.add(cat)
    db.session.commit()
    return 'cat add success'


@blue.route('/adddog')
def add_dog():
    dog = Dog()
    dog.a_name = '傻狗'
    dog.d_legs = '5'
    db.session.add(dog)
    db.session.commit()
    return 'dog add success'


@blue.route('/getcat')
def get_cat():
    # cat = Cat.query.filter(Cat.id.__eq__(
    #     2)).all()  # 使用all方法会把BaseQuery对象转成list对象，只有BaseQuery对象才可以使用filter方法
    # cat = Cat.query.filter(Cat.id.__lt__(3)).all()
    # cat = Cat.query.filter(Cat.id < 3).all()  # 等同于上面这条代码
    # cat = Cat.query.filter(Cat.a_name.contains('猫')).all()  # contains包含操作
    # cat = Cat.query.offset(2).limit(3)
    # cat = Cat.query.offset(3).limit(2)  # offset 和 limit 不区分顺序，都是先offset再limit
    cat = Cat.query.offset(3).limit(2).order_by(Cat.id)
    # cat = Cat.query.order_by(-Cat.id).offset(3).limit(2)
    print(cat)
    print(type(cat))
    return render_template('CatList.html', cats=cat)


@blue.route('/adddogs')
def add_dogs():
    for i in range(20):
        dog = Dog()
        dog.a_name = f'二哈{random.randrange(1000)}'
        db.session.add(dog)
    db.session.commit()
    return 'add success'


@blue.route('/getdogs')
def get_dogs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 4, type=int)

    dogs = Dog.query.offset(per_page * (page - 1)).limit(per_page)

    return render_template('DogList.html', dogs=dogs)


@blue.route('/getdogswithpage')
def get_dogswithpage():
    dogs = Dog.query.paginate().items
    pagination = Dog.query.paginate()
    per_page = request.args.get('per_page', type=int)
    return render_template('DogList.html',
                           dogs=dogs,
                           pagination=pagination,
                           per_page=per_page)


@blue.route('/addcustomer')
def add_customer():
    customer = Customer()
    customer.c_name = f'剁手党{random.randrange(10000)}'
    db.session.add(customer)
    db.session.commit()
    return 'add success'


@blue.route('/addaddress')
def add_address():
    address = Address()
    address.a_position = f'正阳北路{random.randrange(10000)}号'
    # 实现逆序需要使用desc方法或者使用text()方法包裹负号的字段名
    address.a_customer_id = Customer.query.order_by(
        Customer.id.desc()).first().id

    # address.a_customer_id = Customer.query.order_by(db.text('-id')).first().id

    db.session.add(address)
    db.session.commit()
    return 'add success'


@blue.route('/getcustomer')
def get_customer():
    a_id = request.args.get('a_id', type=int)
    address = Address.query.get_or_404(a_id)
    # customer = Customer.query.get(address.a_customer_id)
    customer = address.customer
    print(address.a_customer_id)
    print(customer)
    print(type(customer))
    return customer.c_name


@blue.route('/getaddresses')
def get_addresses():
    c_id = request.args.get('c_id', type=int)
    customer = Customer.query.get(c_id)
    # addresses = Address.query.filter_by(a_customer_id=customer.id)
    addresses = customer.addresses
    print(type(addresses))
    print(addresses)
    return render_template('AddressList.html', addresses=addresses)
