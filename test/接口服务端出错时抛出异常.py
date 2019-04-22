#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

# 接口路由地址
@app.route('/sklearn', methods=['POST'])
def index():
    from sklearn import linear_model
    from sklearn.linear_model import BayesianRidge
    data = request.json
    data = data["data"]
    print(data)
    print(type(data))
    list1 = []
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


    # key1,value = data[0].items()
    # X = value
    # name1 = key1

    # key2, value = data[1].items()
    # Y = value


    print(name2)
    print(type(Y))
    try:
        reg = linear_model.BayesianRidge()
        reg.fit(X, Y)
        BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, compute_score=False, copy_X=True,
                      fit_intercept=True, lambda_1=1e-06, lambda_2=1e-06, n_iter=300,
                      normalize=False, tol=0.001, verbose=False)
        pdic = data[2]['pdic']
        xx = reg.predict([pdic])
        xx = xx.tolist()
    except Exception as e:
        e = str(e)

        return jsonify(erro=e)

    return jsonify(uu={name2: xx},yy={name1:{'N值':12,'均值':name1},name2:{'N值':12,'均值':xx}})


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True,host="192.168.11.220",port=5000)
