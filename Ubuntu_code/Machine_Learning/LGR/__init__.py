#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Blueprint

# 1. 创建蓝图对象
LGR_blue = Blueprint('decision_tree', __name__)

from . import views