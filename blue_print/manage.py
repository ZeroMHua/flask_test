#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# -*- coding:utf-8 -*-

from flask import Flask
from blue_print.users import users_blue
# from orders import orders_blue
from blue_print.goods import goods_blue

app = Flask(__name__)

# 将蓝图注册到app
app.register_blueprint(users_blue)
# app.register_blueprint(orders_blue)
app.register_blueprint(goods_blue, url_prefix='/goods')


@app.route('/')
def index():
    return "index"


if __name__ == '__main__':
    # print(app.url_map)
    app.run(debug=True)
