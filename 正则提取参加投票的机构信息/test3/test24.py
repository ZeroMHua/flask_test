#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
with open("test8.txt","r",encoding="utf-8") as f:
    s = f.read()

# p = re.compile(r'案例名称.*案例名称?')
s1=s.replace('案例名称','88案例名称')
s2 = s1.split('88')
print(len(s2))
for i in s2:
    file = open('test10.txt', 'a', encoding="utf-8")
    file.write(str(i)+"\n")
    file.close()

# result = p.findall(s)
# result = re.findall("案例名称(.*)。.*",s)
# print(len(result))


# file = open('test6.txt', 'a', encoding="utf-8")
# file.writelines(str(s2)+"\n")
# file.close()
