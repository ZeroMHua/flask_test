#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask, jsonify
from flask import request
from numpy import mean, median, ptp, var, std
from scipy.stats import mode
import numpy as np
import json

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    return "你好"

@app.route('/getlist', methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
        list2 = []
        data = request.json
        list1 = data["list1"]
        # 均值
        a1 = mean(list1)
        list2.append(a1)
        # 中位数
        a2 = median(list1)
        list2.append(a2)
        # 众数
        a3 = mode(list1)
        print(a3)
        # 极差
        a4 = ptp(list1)
        a4=str(a4)
        list2.append(a4)
        print(a4)
        # 方差
        a5 = var(list1)
        a5 = str(a5)
        list2.append(a5)
        print(a5)
        # 标准差

    return jsonify(均值=a1, 中位数=a2,极差=a4,方差=a5,数据列表=list2)
    # return jsonify(均值=a1, 中位数=a2, 众数=a3)


if __name__ == '__main__':
    app.run(debug=True)
