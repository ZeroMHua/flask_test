#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from . import users_blue


@users_blue.route("/user_info")
def user_info():
    return "users"
