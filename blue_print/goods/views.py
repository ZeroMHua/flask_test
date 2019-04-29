#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from . import goods_blue


@goods_blue.route("/index")
def user_info():
    return "goods_blue"