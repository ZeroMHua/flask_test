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
    list1 = []
    for key, value in data.items():
        list1.append(key)
    # da1 = [data[key] for key in list1]
    # print(da1)
    # 如果传的参数顺序不变
    # X = [[0., 0.], [1., 1.], [2., 2.], [3., 3.]]
    # X = data["你"]
    X = data[list1[0]]
    # Y = data["Y"]
    Y = data[list1[1]]
    # Y = [0., 1., 2., 3.]
    try:
        reg = linear_model.BayesianRidge()
        reg.fit(X, Y)
        BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, compute_score=False, copy_X=True,
                      fit_intercept=True, lambda_1=1e-06, lambda_2=1e-06, n_iter=300,
                      normalize=False, tol=0.001, verbose=False)
        pdic = data["pdic"]
        xx = reg.predict([pdic])
        xx = xx.tolist()
    except Exception as e:
        e = str(e)

        return jsonify(erro=e)

    return jsonify(xx=xx, Y=Y, uu={list1[1]: 0.35},yy={list1[0]:{'N值':12}})


if __name__ == '__main__':
    app.run(debug=True)
