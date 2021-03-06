#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# -*- coding:utf-8 -*-

from flask import Flask
from blue_print.users import users_blue
from blue_print.orders import orders_blue
from blue_print.kmeans import kmeans_blue
from blue_print.goods import goods_blue
from blue_print.random_tree import random_tree_blue

app = Flask(__name__)

# 将蓝图注册到app
app.register_blueprint(users_blue, url_prefix='/users')
app.register_blueprint(orders_blue,url_prefix='/orders')
app.register_blueprint(goods_blue, url_prefix='/goods')
app.register_blueprint(kmeans_blue, url_prefix='/kmeans')
app.register_blueprint(random_tree_blue,url_prefix='/random_tree')


# @app.route('/')
# def index():
#     return "index"


if __name__ == '__main__':
    # print(app.url_map)
    app.run(debug=True)
    # 启用多线程
    # app.run(debug=False,threaded=True)
    # 启用多进程，但是在win系统下进程数不能超过1，否则报错
    # app.run(processes=1)
