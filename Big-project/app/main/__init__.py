from flask import Blueprint

main = Blueprint('main', __name__)  # 两个参数分别是这个蓝本所处的包，以及该蓝本的文件名
from . import views, errors  # 导入这两个模块来将处理程序与蓝本关联起来，是必需的
