#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
import json

# url = "http://192.168.100.106:5000/sklearn"
url = "http://127.0.0.1:5000/sklearn"
# url = "http://192.168.11.220:5000/sklearn"

data = {
    "data":[
        {"第一个参数": [[0., 0.], [1., 1.], [2., 2.], [3., 3.]]},
        {"第二个参数": [0., 1., 2., 4.]},
        {"pdic": [1, 0.]}
    ]

    # "第一个参数": [[0., 0.], [1., 1.], [2., 2.], [3., 3.]],
    # "第二个参数": [0., 1., 2., 4.],
    # "pdic": [1, 0.]
}
data=json.dumps(data,ensure_ascii=True)
headers = {'Content-Type': 'application/json'}
response = requests.post(url,data,headers=headers)


data1 = response.content.decode(encoding="unicode-escape")


# data1 = response.content.decode(encoding="utf-8")
# data = data.encode("unicode-escape").decode("utf-8")
# data = data.encode("unicode-escape").decode("gb18030")
# 获取key为中文的返回值
data2 = json.loads(data1)
print(data1)

