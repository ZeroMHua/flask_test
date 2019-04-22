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

    X = data[list1[0]]
    Y = data[list1[1]]
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

    return jsonify(uu={list1[1]: xx},yy={list1[0]:{'N值':12,'均值':list1[0]},list1[1]:{'N值':12,'均值':xx}})


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True,host="192.168.100.106",port=5000)
