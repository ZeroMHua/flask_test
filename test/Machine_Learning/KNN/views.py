#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua


from . import KNN_blue

@KNN_blue.route("/test",methods=['POST'])
def KNNS():
    from flask import jsonify
    from flask import request
    data = request.json
    filename = data['data'][0]["filename"]
    print(data)
    return jsonify(yy=filename)


