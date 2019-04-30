#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import jsonify, request

from . import kmeans_blue

# 2 使用蓝图注册路由
@kmeans_blue.route('/sklearn', methods=['POST'])
def index():
    import numpy as np
    data = request.json
    data = data["data"]

    keys = list(data[0].keys())

    values = list(data[0].values())

    n = len(keys)
    list1 = [[] for _ in range(n)]
    list2 = [[] for _ in range(n)]

    a2 = {"parentTitle": "",
          "parentContent": [],
          "title": "",
          "content": [],
          "rowTop": "",
          "colTop": "",
          "rowNames": [],
          "combination": False,
          "colNames": ['均值差', 't值', 'p值', '样本1均值', '样本2均值'],
          "values": []
          }
    data1 = []
    pic_list = []

    for i in range(n):

        X = values[i]

        name1 = keys[i]

        list1[i] = [[] for _ in range(3)]

        # 方法一
        qq = i*9
        ww = i+6
        list1[i][0].append(qq)
        list1[i][0].append(ww)
        # 方法二
        q2 = i+1
        w2 = i+2
        list1[i][1].append(q2)
        list1[i][1].append(w2)
        # 方法三
        q3 = i+i*5
        w3 = i*8
        list1[i][2].append(q3)
        list1[i][2].append(w3)

        pic_url = "www."+name1+".com"





        # 先创建前n个表

        a = {"parentTitle": "",
             "parentContent": [],
             "title": "",
             "content": [],
             "rowTop": "",
             "colTop": "",
             "rowNames": [x for x in range(1, n + 1)],
             "combination": False,
             "colNames": ['N值', '均值'],
             "values": []
             }
        pic ={
            "parentTitle": "",
            "title": "",
            "type": ".png",
            "path": "",
            "dependPath": "",
            "content": [{}],
            "params": {},
            "reload": False
        }

        a["values"].append(list1[i])
        a["title"] = name1
        data1.append(a)

        a2['values'].append(list2[i])
        a2["titles"] = keys
        pic["title"] = name1+"QQ图"
        pic['path'] = pic_url
        pic_list.append(pic)

    data1.append(a2)
    aq = [{"code": 0,
           "message": None,
           "varInfos": None,
           "mData": None,
           "fields": [],
           "rFiles": [],
           "tables": []}]
    aq[0]["tables"] = data1
    aq[0]["rFiles"] = pic_list


    # print(aq)
    return jsonify(yy={"data": aq

                       })