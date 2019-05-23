#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask
from KNN import KNN_blue
from test import test_blue
from LGR import LGR_blue
from SVM import SVM_blue
from decision_tree import DST_blue
from random_forest import RDF_blue

app = Flask(__name__)

# 将蓝图注册到app
app.register_blueprint(KNN_blue, url_prefix='/KNNS')
app.register_blueprint(test_blue, url_prefix='/test')
app.register_blueprint(LGR_blue, url_prefix='/LGRS')
app.register_blueprint(SVM_blue,url_prefix='/SVMS')
app.register_blueprint(DST_blue,url_prefix='/DSTS')
app.register_blueprint(RDF_blue,url_prefix='/RDFS')

if __name__ == '__main__':
    # print(app.url_map)
    app.run(debug=True)
    # app.run(debug=False, host="192.168.100.106", port=5000)
    # 启用多线程
    # app.run(debug=False,threaded=True)
    # 启用多进程，但是在win系统下进程数不能超过1，否则报错
    # app.run(processes=1)