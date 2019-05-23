#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
import json
import time
# url = "http://192.168.100.106:5000/sklearn"
url = "http://192.168.100.106:5000/SVMS/SVM"
# url = "http://127.0.0.1:5000/SVMS/SVM"
# url = "http://192.168.11.220:5000/sklearn"
start_time = time.time()
data = {
    "data": [
        {"filename": "420testdata.csv","kernel":"linear","C":0.5,"gamma":0.5},
        {"tab_list":['住院天数', '年龄', '咳嗽', '流涕', '呼吸音粗', '性别'],"vars_c":['住院天数', '年龄'],"vars_d":['咳嗽', '流涕', '呼吸音粗'],"target":['性别']}
        # {"vars_c":['住院天数', '年龄']},
        # {"vars_d":['咳嗽', '流涕', '呼吸音粗']},
        # {"target":['性别']},
        # {"testdata":None},
        # {"n_neighbors":6}
    ]
}
data = json.dumps(data, ensure_ascii=True)
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data, headers=headers)

data1 = response.content.decode(encoding="unicode-escape")
# data1 = response.content.decode(encoding="utf-8")

# 获取key为中文的返回值
# data2 = json.loads(data1)
# 提取第一个表的信息
# data3 = data2["yy"]
print(data1)
end_time = time.time()
times = end_time - start_time
print(times)
