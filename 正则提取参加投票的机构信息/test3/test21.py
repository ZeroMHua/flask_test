#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
with open("test4.txt","r",encoding="utf-8") as f:
    # s = f.read()
    s= f.readlines()
    for k in s:
        if "查看详情" not in k:
            # file = open('test5.txt', 'wb')
            file = open('test5.txt', 'a', encoding="utf-8")
            file.writelines(str(k)+"\n")
            file.close()

# file.writelines(a + "\n")
    # print(s)
# s1 = s.strip()
# s2 = s1.lstrip()
# s3 = s2.rstrip()
# s4=s3.replace(' ','')
# print(s4)
# file = open('test4.txt', 'wb')
# file.write(str(s4).encode("utf-8"))
# file.close()