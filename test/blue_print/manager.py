#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua

from flask_script import Manager
from ..blue_print.info import create_app
# from .info import create_app
app = create_app('development')
# 创建Manager对象
manager = Manager(app)

# 添加命令行迁移命令db
@app.route('/index')
def index():
    return 'index'


if __name__ == '__main__':
    manager.run()