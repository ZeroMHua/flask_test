#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
import json
import numpy as np
import pandas as pd
url = "http://127.0.0.1:5000/clusters"
# url = "http://192.168.11.220:9900/ochiias"
filename = "admin2.csv"
# 获取数据源
# print("start to read file")
case_train = np.genfromtxt("{}".format(filename), delimiter=',')

# 去除第一行和第一列(如果有字段名的话)
case_train = np.delete(case_train, 0, axis=0)
# print(case_train1)
case_train1 = np.array(case_train)
# print(case_train1)
# 将矩阵反转为a
a = case_train1.T
# numpy对象无法被json序列化作为参数传进去，
# 因此先转化为list,接口那边接收到后再转为numpy对象
a = a.tolist()

# 读取关键字
keywords = pd.read_csv("{}".format(filename), nrows=0)
keywords = keywords.columns
keywords = list(keywords)

data = {
        # "list1":[x for x in range(1000000)]
        # "list1":[93,62,51,93,75,82,93,62,65,51,86,89,100]
    "case_train":a,
    "keywords":keywords,
    "heights":42
}
data=json.dumps(data,ensure_ascii=True)
headers = {'Content-Type': 'application/json'}
response = requests.post(url,data,headers=headers)
data1 = response.content.decode(encoding="unicode-escape")
# data1 = response.content.decode(encoding="utf-8")

# data = data.encode("unicode-escape").decode("utf-8")
# data = data.encode("unicode-escape").decode("gb18030")
print(data1)
