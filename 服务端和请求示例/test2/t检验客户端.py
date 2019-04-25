#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
import json

url = "http://192.168.100.106:5100/sklearn"
# url = "http://127.0.0.1:5000/sklearn"
# url = "http://192.168.11.220:5000/sklearn"

data = {
    "data": [
        {"qqq": [x for x in range(10)],
         "www": [y for y in range(110, 121)],
         "eee": [z for z in range(20, 31)],
         "ttt": [z for z in range(20, 31)]
         # "第4个参数": [z for z in range(120, 131)],
         # "第5个参数": [z for z in range(210, 311)]
         },
        {"rrr": 0.95}
    ]
}
data = json.dumps(data, ensure_ascii=True)
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data, headers=headers)

data1 = response.content.decode(encoding="unicode-escape")

# 获取key为中文的返回值
data2 = json.loads(data1)
# 提取第一个表的信息
data3 = data2["yy"]
print(data1)
