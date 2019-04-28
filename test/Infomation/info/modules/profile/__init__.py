from flask import Blueprint

# 1. 创建蓝图对象
profile_blu = Blueprint('profile', __name__)

from . import views