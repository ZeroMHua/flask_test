from flask import Blueprint

# 1. 创建蓝图对象
DST_blue = Blueprint('DST', __name__)

from . import views