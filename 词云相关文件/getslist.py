#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask, jsonify
from flask import request
import numpy as np
import json

app = Flask(__name__)


@app.route('/getlist', methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
        data = request.json
        print(data["list1"])
        keywords = data["kw"]
        print(keywords)
        list1 = data["list1"]
        list2 = np.array(list1)
        list3 = list2.T
        print(list2)
        print(list3)

    return jsonify(keywords=data["kw"], list1=list1)


if __name__ == '__main__':
    app.run(debug=True)
