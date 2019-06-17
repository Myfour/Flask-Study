import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-nerver-guess'

OPENID_PROVIDERS = [{
    'name': 'Google',
    'url': 'https://www.google.com/accounts/o8/id'
}, {
    'name': 'Yahoo',
    'url': 'https://me.yahoo.com'
}, {
    'name': 'AOL',
    'url': 'http://openid.aol.com/<username>'
}, {
    'name': 'Flickr',
    'url': 'http://www.flickr.com/<username>'
}, {
    'name': 'MyOpenID',
    'url': 'https://www.myopenid.com'
}]

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                                                      'app.db')  # 设置sqlite文件位置
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,
                                       'db_repository')  # 设置迁移数据库的信息的文件夹
