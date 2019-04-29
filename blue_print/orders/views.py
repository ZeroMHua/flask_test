#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from . import orders_blue


@orders_blue.route("/info")
def user_info():
    return "orders"