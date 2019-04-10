#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
import json
url = "http://127.0.0.1:5000/getlist"
data = {
        "list1":[93,62,51,93,75,82,93,62,65,51]
}
data=json.dumps(data,ensure_ascii=False)

headers = {'Content-Type': 'application/json'}
response = requests.post(url,data,headers=headers,)
data = response.content.decode(encoding="gb18030").encode("gb18030").decode("gb18030")
# data = data.encode("utf-8").decode("gb18030")
print(data)