#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
with open("TEST2.txt","r",encoding="utf-8") as f:
    s = f.read()

# s1=s.replace('医疗健康人工智能应用落地优秀案例投票医疗健康人工智能应用落地优秀案例投票秒题请至少选择一个案例进行投票谢谢多选题','')
print(s)
# s2 =s.split("查看详情")
p = re.compile(r'华文仿宋.*?查看详情?')
su = p.findall(s)
print(len(su))
for i in su:
    print(i)
# p = re.compile(r'"objURL":"http.*?jp[e]?g"')
#         b = re.compile(r'"http.*?jpg"')
#         result = p.findall(page)
# for k in s2:
#     print(k)