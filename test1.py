#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask, jsonify
from flask import request
import json
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print('请求方式为------->', request.method)
    args = request.args.get("name") or "args没有参数"

    print('args参数是------->', args)
    form = request.form.get('name') or 'form 没有参数'
    print('form参数是------->', form)
    print(type(form))
    return jsonify(args=args, form=form)


@app.route('/list1', methods=['GET', 'POST'])
def server():
    list1 = request.form.getlist("list1")  # 由于返回的是数组，要写成 'list[]'
    print(list1)

    return jsonify(list1=list1)  # 一定要有返回值


@app.route('/get_age/<int:age>/', methods=['GET', 'POST'])
def hello_int(age):
    return 'hello int:%s' % (age)

@app.route('/getrequest/', methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
        #form = request.form
        # data = request.data
        # data = data.decode()
        # data = json.loads(data)
        data = request.json
        print(data)
        print(data["pass"])
        print(data["list1"])
        print(type(data))
    return jsonify(list1="pass")



if __name__ == '__main__':
    app.run(debug=True)
