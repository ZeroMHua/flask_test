#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
import requests
from lxml import etree
import time

url="https://tp.wjx.top/m/38988708.aspx?from=singlemessage"
response = requests.get(url)
data = response.content.decode(encoding="utf-8")
# data = response.content
p = '[^a-zA-Z0-9]'
# p = '[\u4e00-\u9fa5]+'
result = re.findall(p, data)
s1 = "".join(result)


file = open('test2.txt', 'wb')
file.write(str(s1).encode("utf-8"))
file.close()



# html = etree.HTML(data)
# p = re.compile(r'\w"')
# b = re.compile(r'"http.*?jpg"')
# result = p.findall(data)


