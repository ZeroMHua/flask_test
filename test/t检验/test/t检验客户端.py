#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
import json

# url = "http://192.168.100.106:5000/sklearn"
url = "http://localhost:12345/group/addGroup?groupName=12&projectId=33"
# url = "http://192.168.11.220:5000/sklearn"

# data = {
#     "data":[
#         {"第1个参数": [x for x in range(10)]},
#         {"第2个参数": [y for y in range(10,21)] },
#         ]
# }
# data=json.dumps(data,ensure_ascii=True)
headers = {'Content-Type': 'application/json'}
# User-Agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
response = requests.post(url)

data1 = response.content.decode(encoding="unicode-escape")

# 获取key为中文的返回值
data2 = json.loads(data1)
print(data2)

