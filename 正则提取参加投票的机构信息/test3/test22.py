#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
with open("test5.txt","r",encoding="utf-8") as f:
    s = f.read()
s1 = s.replace('华文仿宋','')
s2 = s1.replace('仿宋','')
print(s2)
file = open('test6.txt', 'a', encoding="utf-8")
file.writelines(str(s2)+"\n")
file.close()
