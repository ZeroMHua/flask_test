#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
with open("TEST2.txt","r",encoding="utf-8") as f:
    s = f.read()
print(s)
s1=s.replace('医疗健康人工智能应用落地优秀案例投票医疗健康人工智能应用落地优秀案例投票秒题请至少选择一个案例进行投票谢谢多选题','')
print(s1)
s2 =s1.split("查看详情")
print(s2[1])
file = open('s3.txt', 'wb')
file.write(str(s2[1]).encode("utf-8"))
file.close()