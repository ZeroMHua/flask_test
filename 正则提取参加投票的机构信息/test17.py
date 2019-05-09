#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
with open("s3.txt","r",encoding="utf-8") as f:
    s = f.read()
print(s)
s1=s.replace('案例名称','案例名称:')
s2=s1.replace('仿宋申报单位仿宋',' 申报单位:')
s3=s2.replace('仿宋实施厂商仿宋',' 实施厂商:')
s4=s3.replace('仿宋一申报类型一华文仿宋','  一·申报类型:')
s5=s4.replace('华文仿宋二案例基本情况华文仿宋','  二·案例基本情况:')
s6=s5.replace('华文仿宋三使用效果华文仿宋','  三·使用效果:')
s7=s6.replace('华文','')
s8=s7.replace('仿宋','')
s9 = s8.split(' ')
name = s9[1].replace('申报单位:','')
for a in s9 :

    file = open('{}.txt'.format(name), 'a',encoding="utf-8")
    # file.write(str(a).encode("utf-8"))
    # file.write('\\n')

    file.writelines(a + "\n")

    file.close()

# print(s9)
# # s2 =s1.split("查看详情")
# print(s2[1])
# file = open('s5.txt', 'wb')
# file.write(str(s8).encode("utf-8"))
# file.close()