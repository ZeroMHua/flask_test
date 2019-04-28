#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from . import index_blu
@index_blu.route('/index',methods=['GET', 'POST'])
def index():
    return "index"