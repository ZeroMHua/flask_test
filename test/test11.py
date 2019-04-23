#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
a = {
    "code": 0,
    "message": None,
    "varInfos": None,
    "mData": None,
    "fields": [],
    "rFiles": [],
    "tables": [{"parentTitle": "",
                "parentContent": [],
                "title": "正态性检验",
                "content": [],
                "rowTop": "",
                "colTop": "",
                "rowNames": [1, 2],
                "combination": False,
                "colNames": ['N值', '均值', '标准差', '最小值', '最大值', '75%位数'],
                "values": []
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
data1 = data[0]

print(data1)