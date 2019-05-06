#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask, jsonify
from flask import request
from scipy.stats import ttest_ind

app = Flask(__name__)


# 接口路由地址
@app.route('/sklearn', methods=['POST'])
def index():
    import numpy as np
    data = request.json
    data = data["data"]
    print(data)
    print(data[0])
    print(data[1])
    for key1, value in data[0].items():
        # list1.append(key)

        global X
        X = value
        global name1
        name1 = key1

    for key2, value2 in data[1].items():
        # list1.append(key)
        global Y
        Y = value2

        global name2
        name2 = key2

    try:
        # 均值
        xx = np.mean(X)
        yy = np.mean(Y)
        # 均值差
        if xx > yy:
            jzc = xx - yy
        else:
            jzc = yy - xx
        # 标准差
        bzc = np.std(X, ddof=1)
        bzc = round(bzc, 2)
        bzc2 = np.std(Y, ddof=1)
        bzc2 = round(bzc2, 2)
        # 最小值
        zxz = min(X)
        zxz2 = min(Y)
        # 最大值
        zdz = max(X)
        zdz2 = max(Y)
        # 百分数数 5%位数
        """
        第一步：排序
        第二步：计算 百分位数所在区间上限下限，(数组索引从0开始)，若下限等于本身，则减1
        第三步：上下限即索引，根据索引求出区间，根据线性插值加下限值 即为所求百分位数
        """
        X = sorted(X)
        num = len(X)
        N = num - 1
        print(N)
        # 计算百分位数
        P = 75  # 百分位数
        floor1 = int(np.floor(N / 100 * P))
        ceil1 = int(np.ceil(N / 100 * P))
        if floor1 == ceil1:
            floor1 -= 1
        bfw = X[floor1] + (X[ceil1] - X[floor1]) * (N / 100 * P - floor1)  # also np.percentile(b,10)

        Y = sorted(Y)
        num2 = len(Y)
        N2 = num2 - 1
        print(N2)
        # 计算百分位数
        P2 = 75  # 百分位数
        floor12 = int(np.floor(N2 / 100 * P2))
        ceil12 = int(np.ceil(N2 / 100 * P2))
        if floor12 == ceil12:
            floor12 -= 1
        bfw2 = X[floor12] + (X[ceil12] - X[floor12]) * (N2 / 100 * P2 - floor12)  # also np.percentile(b,10)

        # ttest_ind 默认为方差齐性的，equal_var = false 可以设置为方差不齐性。
        t, p = ttest_ind(X, Y, equal_var=False)
        print(ttest_ind(X, Y, equal_var=False))

    except Exception as e:
        e = str(e)
        return jsonify(erro=e)
    # return jsonify(yy={name1: {'N值': 12, '均值': xx, '标准差': bzc, '最小值': zxz, '75%位数': bfw, '最大值': zdz},
    #                    name2: {'N值': 13, '均值': yy, '标准差': bzc2, '最小值': zxz2, '75%位数': bfw2, '最大值': zdz2},
    #                    '配对t检验': {'均值差': jzc, 't值': round(t,2), 'p值': round(p, 8), '样本1均值': xx, '样本2均值': yy}
    #                    })
    return jsonify(yy={"data": [
        {
            "code": 0,
            "message": None,
            "varInfos": None,
            "mData": None,
            "fields": [],
            "rFiles": [],
            "tables": [{"parentTitle": "",
                        "parentContent": [
                        ],
                        "title": name1+"正态性检验",
                        "content": [
                        ],
                        "rowTop": "",
                        "colTop": "",
                        "rowNames": [1, 2],
                        "combination": False,
                        "colNames": ['N值', '均值', '标准差', '最小值', '75%位数', '最大值'],
                        "values": [[12, xx, bzc, zxz, bfw, zdz], [13, yy, bzc2, zxz2, bfw2, zdz2]]},
                       {"parentTitle": "N (均数) 方差",
                        "parentContent": [],
                        "title": "t检验",
                        "content": [],
                        "rowTop": "",
                        "colTop": "",
                        "rowNames": [1, 2],
                        "combination": False,
                        "colNames": ['均值差', 't值', 'p值', '样本1均值', '样本2均值'],
                        'values': [jzc, round(t, 2), round(p, 8), xx, yy]}
                       ]
        }]

    })


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True,host="192.168.11.220",port=5000)
