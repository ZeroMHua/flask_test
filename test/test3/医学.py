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
p = '[\u4e00-\u9fa5]+'
result = re.findall(p, data)
s1 = "".join(result)
s2 = "医疗健康人工智能应用落地优秀案例投票医疗健康人工智能应用落地优秀案例投票秒题请至少选择一个案例进行投票谢谢多选题"
s3 = s2.replace('医疗','')
print(s3)

strinfo = re.compile('医疗健康')
b = strinfo.sub('',s2)
print(b)



# file = open('TEST2.txt', 'wb')
# file.write(str(s1).encode("utf-8"))
# file.close()



# html = etree.HTML(data)
# p = re.compile(r'\w"')
# b = re.compile(r'"http.*?jpg"')
# result = p.findall(data)


