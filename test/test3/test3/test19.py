#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
with open("test3.txt","r",encoding="utf-8") as f:
    s = f.read()
    # s= f.readlines()
    # print(s)
s1 = s.strip()
s2 = s1.lstrip()
s3 = s2.rstrip()
s4=s3.replace(' ','')
print(s4)
file = open('test4.txt', 'wb')
file.write(str(s4).encode("utf-8"))
file.close()