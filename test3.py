#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
import json
url = "http://192.168.11.220:9900/getstr"
data = {
        # "list1":[x for x in range(1000000)]
        # "list1":[93,62,51,93,75,82,93,62,65,51,86,89,100]
    "str1":12,
    "str2":["你好","大"]

}
data=json.dumps(data,ensure_ascii=True)

headers = {'Content-Type': 'application/json'}
response = requests.post(url,data,headers=headers)
data1 = response.content.decode(encoding="unicode-escape")
# data1 = response.content.decode(encoding="utf-8")

# data = data.encode("unicode-escape").decode("utf-8")
# data = data.encode("unicode-escape").decode("gb18030")
print(data1)