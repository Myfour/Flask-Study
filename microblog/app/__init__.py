from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views  # 不能缺少 少了会出错