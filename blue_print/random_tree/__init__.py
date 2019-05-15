#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Blueprint

# 1. 创建蓝图对象
random_tree_blue = Blueprint('random_tree', __name__)

from . import views