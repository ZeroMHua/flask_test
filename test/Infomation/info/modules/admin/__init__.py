from flask import Blueprint

# 1. 创建蓝图对象
admin_blu = Blueprint('admin', __name__)

from . import views