#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
with open("test6.txt","r",encoding="utf-8") as f:
    # s = f.read()
    s=f.readlines()
    print(s)
    for k in s:
        if "\n" in k:
            s1 = k.replace('\n','')
            print(s1)
            file = open('test8.txt', 'a', encoding="utf-8")
            file.write(str(s1))
            file.close()
# p = re.compile(r'案例名称.\S*。?')


# result = p.findall(s)
# result = re.findall("案例名称(.*)。.*",s)
# print(result)

# file = open('test6.txt', 'a', encoding="utf-8")
# file.writelines(str(s2)+"\n")
# file.close()
