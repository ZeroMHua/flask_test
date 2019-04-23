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
    keys = list(data[0].keys())
    values = list(data[0].values())
    print(keys)
    print(values)
    n = len(keys)
    list1 = [[] for _ in range(n-1)]
    print(list1)
    list2 = []

    for i in range(n-1):
        global X
        X = values[i]
        global name1
        name1 = keys[i]


        try:
            # N值
            nz = 12
            list1[i].append(nz)
            # 均值
            xx = np.mean(X)
            list1[i].append(xx)

            # 均值差

            jzc = 0
            list1[i].append(xx)
            # 标准差
            bzc = np.std(X, ddof=1)
            bzc = round(bzc, 2)
            list1[i].append(bzc)

            # 最小值
            zxz = min(X)
            list1[i].append(zxz)

            # 最大值
            zdz = max(X)
            list1[i].append(zdz)
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

            list1.append(bfw)
            a = {
            "code": 0,
            "message": None,
            "varInfos": None,
            "mData": None,
            "fields": [],
            "rFiles": [],
            "tables": [{"parentTitle": "",
                        "parentContent": [],
                        "title": name1+"正态性检验",
                        "content": [],
                        "rowTop": "",
                        "colTop": "",
                        "rowNames": [1, 2],
                        "combination": False,
                        "colNames": ['N值', '均值', '标准差', '最小值','最大值' ,'75%位数'],
                        "values": [list1[i]]
                        }
                       # {"parentTitle": "",
                       #  "parentContent": [],
                       #  "title": name1+"t检验",
                       #  "content": [],
                       #  "rowTop": "",
                       #  "colTop": "",
                       #  "rowNames": keys,
                       #  "combination": False,
                       #  "colNames": ['均值差', 't值', 'p值', '样本1均值', '样本2均值'],
                       #  'values': [jzc, round(t, 2), round(p, 8), xx, yy]}
                       ]
                }
            data = [a for _ in range(2)]
            data[i]['code'] = 200



        except Exception as e:
            e = str(e)
            return jsonify(erro=e)
    return jsonify(yy={"data": data

    })


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True,host="192.168.11.220",port=5000)
