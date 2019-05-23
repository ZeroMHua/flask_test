#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Blueprint

# 1. 创建蓝图对象
SVM_blue = Blueprint('SVM', __name__)

from . import views