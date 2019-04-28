from flask import Blueprint

# 1. 创建蓝图对象
news_blu = Blueprint('news', __name__)

from . import views