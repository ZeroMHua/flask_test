#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask

# 创建Flask应用程序实例
def create_app(config_name):
    app = Flask(__name__)
    # 3. 使用app对象注册蓝图
    from ..info.modules.index import index_blu
    app.register_blueprint(index_blu)

    return app
