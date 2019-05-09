#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
with open("TEST2.txt","r",encoding="utf-8") as f:
    s11 = f.read()

# s1=s.replace('医疗健康人工智能应用落地优秀案例投票医疗健康人工智能应用落地优秀案例投票秒题请至少选择一个案例进行投票谢谢多选题','')

s2 =s11.split("查看详情")
name = 0
for s in s2:
    s1 = s.replace('案例名称', '案例名称:')
    s2 = s1.replace('仿宋申报单位仿宋', ' 申报单位:')
    s3 = s2.replace('仿宋实施厂商仿宋', ' 实施厂商:')
    s4 = s3.replace('仿宋一申报类型一华文仿宋', '  一·申报类型:')
    s5 = s4.replace('华文仿宋二案例基本情况华文仿宋', '  二·案例基本情况:')
    s6 = s5.replace('华文仿宋三使用效果华文仿宋', '  三·使用效果:')
    s7 = s6.replace('华文', '')
    s8 = s7.replace('仿宋', '')
    s9 = s8.split(' ')
    # name = s9[1].replace('申报单位:', '')
    name =name+1

    for a in s9:

        file = open('{}.txt'.format(name), 'a', encoding="utf-8")
        # file.write(str(a).encode("utf-8"))
        # file.write('\\n')

        file.writelines(a + "\n")

        file.close()