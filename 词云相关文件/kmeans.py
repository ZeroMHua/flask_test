#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import numpy as np
import sys

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


# 接收外部传入的参数
filename = sys.argv[1]
# filename = "admin2.csv"
# 获取数据源
# print("start to read file")
case_train = np.genfromtxt("{}".format(filename), delimiter=',',encoding="utf-8")
case_train1 = np.delete(case_train,0,axis=0)
try:
    v = pd.read_csv("{}".format(filename),header=None,encoding="utf-8")
except Exception as e:
    print(e)

# 读取关键字
keywords = pd.read_csv("{}".format(filename), nrows=0,encoding="utf-8")
keywords = list(keywords)
# 去除第一行和第一列(如果有字段名的话)
case_train = np.delete(case_train,0,axis=0)
case_train1=np.array(case_train)
# 将矩阵反转为a
a = case_train1.T

# print(a)

global list1
global list3
global list4
global list6
global data_list

list1 = []
list3 = []
list4 = []
list6 = []
data_list = []
total_dic = {}
for i in a:
    for k in a:
        c = [i,k]

        # 对两个矩阵对比后，得到的矩阵求和(AB共同出现的频率)
        # 求每两行的最小值(AB交集的最小值)
        ik = np.min(c, axis=0)
        sum_two = ik.sum()
        list3.append(sum_two)
n = len(a)
# 两两共现的词频矩阵
data_save = [list3[i:i + n] for i in range(0, len(list3), n)]

data_save = np.array(data_save)

# 加关键词后的相似矩阵
# data_save = DataFrame(data_save,index=keywords,columns=keywords)
clf = PCA(n_components=2)
data_save = clf.fit_transform(data_save)

# 构造聚类器，构造一个聚类数为n的聚类器,也就是聚类树形图分类数
estimator = KMeans(n_clusters=3)
# 聚类
estimator.fit(data_save)
# 获取聚类标签
label_pred = estimator.labels_

# 颜色的分类
mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
# 获取聚类中心
centroids = estimator.cluster_centers_
# 获取聚类准则的总和
inertia = estimator.inertia_

data_save = data_save.T
# print(data_save)
x = data_save[0]
y = data_save[1]
fig = plt.figure(figsize=(30, 25),dpi=80)

plt.scatter(x, y)
# 这里xy是需要标记的坐标，xytext是对应的标签坐标
for i in range(len(x)):
    plt.annotate(keywords[i], xy = (x[i], y[i]), xytext = (x[i]+0.1, y[i]+0.1))
picname = filename.replace(".csv","")
picname = picname+"_kmeans.png"
plt.savefig(picname)
