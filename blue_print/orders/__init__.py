#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# Author:hua
from flask import Blueprint

# 1. 创建蓝图对象
orders_blue = Blueprint('orders', __name__)

from . import views