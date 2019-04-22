# -*- coding:utf-8 -*-
# Author:hua
from copy import deepcopy
import numpy as np
import math
import sys
import json
#importlib.reload(sys)
import pandas as pd
from pandas.core.frame import DataFrame

# filename = "/data/wordcloud/python/test/pyfiles/datas5.csv"

# filename = sys.argv[1]
#
filename = "admin2.csv"
# 获取数据源
# print("start to read file")
case_train = np.genfromtxt("{}".format(filename), delimiter=',',encoding="utf-8")
print case_train
case_train1 = np.delete(case_train,0,axis=0)
try:
    v = pd.read_csv("{}".format(filename),header=None,encoding="utf-8")
    print v
except Exception as e:
    print(e)

# 读取关键字
keywords = pd.read_csv("{}".format(filename), nrows=0,encoding="utf-8")
keywords = keywords.columns
keywords = list(keywords)
# print(keywords)
# keywords1 = []
# for jj in keywords:
#    # print jj
#     if "\\u" in jj:
# 	print 2222
#     jj = jj.encode('unicode-escape')
#     bb = jj.decode('unicode-escape')
#
#     keywords1.append(bb)
# 去除第一行和第一列(如果有字段名的话)
case_train = np.delete(case_train,0,axis=0)
# print(case_train1)
case_train1=np.array(case_train)
# print(case_train1)
# 将矩阵反转为a
a = case_train1.T

# print(a)

global list1
global list4
global list6
global data_list

list1 = []
list4 = []
list6 = []
list7 = []
data_list = []
total_dic = {}
for i in a:
    for k in a:
        c = [i,k]

        # print(c)
        # 求每两行的最小值(AB交集的最小值)
        ik = np.min(c, axis=0)
        # print(ik)
        sum_i = i.sum()
        # print(sum_i)
        sum_k = k.sum()
        # 对两个矩阵对比后，得到的矩阵求和(AB共同出现的频率)
        sum_two = ik.sum()
        # 关键词i出现频率总和的平方根
        sqrt_i = math.sqrt(sum_i)
        # 关键词k出现频率总和的平方根
        sqrt_k = math.sqrt(sum_k)
        # ochiia 系数
        ochiia = sum_two/(sqrt_i*sqrt_k)
        # print(ochiia)
        # 相异矩阵系数
        b2 = 1 - ochiia
        # 保留三位小数
        b2 = round(b2, 3)
        list1.append(b2)
n = len(a)
# 将相异矩阵组合成相异系数矩阵
data_save = [list1[i:i + n] for i in range(0, len(list1), n)]

data_save = np.array(data_save)

# 加关键词后的相似矩阵
data_save = DataFrame(data_save,index=keywords,columns=keywords)

for ii in keywords:
    # ii = ii.encode("gbk")
    # print(ii)

    for kk in keywords:
        ds = data_save.loc[ii, kk]
        nn = 1
        if nn <= n:
            # dic = {"name":ii,kk:ds}
            # kk = kk.decode("gbk")
            dic = {kk:ds}
	   
	    
            list4.append(dic)

# 组合成java想要的输出格式
global ff
ff = [list4[i:i + n] for i in range(0, len(list4), n)]
# 添加name这个key
for i in range(n):
    dic4 = {"name":keywords[i]}
    ff[i].append(dic4)

for k in range(len(ff)):
    for i in ff[k]:
        for i, j in i.items():
            total_dic[i] = j
    t = deepcopy(total_dic)

    t1 = json.dumps(t)


    t2 = eval(t1)
    #print(t2)

    t1=t1.decode("unicode-escape")

    # print type(t1)

    # print t1
    data_list.append(t1)
data_list = str(data_list)


data_list = data_list.decode("unicode-escape")
data_list = data_list.replace("u'","")
data_list = data_list.replace("'","")
data_list = data_list.encode('utf-8')

try:
    print data_list
except Exception as e:
    print(e)

# numpy将结果写入文件
# np.savetxt('20.csv',data_save,delimiter=',',fmt = ['%s']*data_save.shape[1],newline = '\n')
# 返回



