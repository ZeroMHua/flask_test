#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Blueprint

# 1. 创建蓝图对象
test_blue = Blueprint('test', __name__)

from . import views