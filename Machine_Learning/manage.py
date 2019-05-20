#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask
from Machine_Learning.KNN import KNN_blue

app = Flask(__name__)

# 将蓝图注册到app
app.register_blueprint(KNN_blue, url_prefix='/KNNS')

if __name__ == '__main__':
    # print(app.url_map)
    app.run(debug=True)
    # 启用多线程
    # app.run(debug=False,threaded=True)
    # 启用多进程，但是在win系统下进程数不能超过1，否则报错
    # app.run(processes=1)