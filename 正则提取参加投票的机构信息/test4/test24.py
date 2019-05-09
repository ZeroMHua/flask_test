#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
with open("test10.txt","r",encoding="utf-8") as f:
    s = f.readlines()
    name = 0
    for s1 in s:
        s2 = s1.replace('申报单位','88申报单位')
        s3 = s2.replace('实施厂商','88实施厂商')
        s4 = s3.replace('一、申报类型','88一、申报类型')
        s5 = s4.replace('二、案例基本情况','88二、案例基本情况')
        s6 = s5.replace('三、使用效果','88三、使用效果')

        s7 = s6.split('88')
        name= s7[1].replace('申报单位：','')
        for k in s7:


            file = open('./txt2/{}.txt'.format(name), 'a', encoding="utf-8")
            file.writelines(str(k)+"\n")
            file.close()

            # print(s7)

# p = re.compile(r'案例名称.*案例名称?')
# s1=s.replace('案例名称','88案例名称')
# s2 = s1.split('88')
# print(len(s2))
# for i in s2:
#     file = open('test10.txt', 'a', encoding="utf-8")
#     file.write(str(i)+"\n")
#     file.close()

# result = p.findall(s)
# result = re.findall("案例名称(.*)。.*",s)
# print(len(result))


# file = open('test6.txt', 'a', encoding="utf-8")
# file.writelines(str(s2)+"\n")
# file.close()
