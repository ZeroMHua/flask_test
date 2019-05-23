from flask import Blueprint

# 1. 创建蓝图对象
RDF_blue = Blueprint('RDF', __name__)

from . import views