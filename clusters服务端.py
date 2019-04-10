#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask, jsonify
from flask import request
from scipy import cluster
import numpy as np
from scipy.cluster import hierarchy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "clusters算法"


@app.route('/clusters', methods=['GET', 'POST'])
def getstr():
    data = request.json
    a = data["case_train"]
    a = np.array(a)
    # # 去除第一行和第一列(如果有字段名的话)
    # case_train = np.delete(case_train, 0, axis=0)
    # # print(case_train1)
    # case_train1 = np.array(case_train)
    # # print(case_train1)
    # # 将矩阵反转为a
    # a = case_train1.T

    keywords = data["keywords"]
    print(keywords)
    # keywords = keywords.columns
    # keywords = list(keywords)
    heights = data["heights"]

    global list3
    global list4
    global list5
    global list6
    global keywords2

    list3 = []
    list4 = []
    list5 = []
    list6 = []
    keywords2 = []
    for i in a:
        for k in a:
            c = [i, k]

            # 求每两行的最小值(AB交集的最小值)
            ik = np.min(c, axis=0)

            # 对两个矩阵对比后，得到的矩阵求和(AB共同出现的频率)
            sum_two = ik.sum()
            list3.append(sum_two)

    n = len(a)
    # 将相似矩阵组合成相似系数矩阵
    data_two = [list3[i:i + n] for i in range(0, len(list3), n)]
    # 构建两两的词频共现矩阵
    data_two = DataFrame(data_two, index=keywords, columns=keywords)
    # 生成聚类树形图
    fig = plt.figure(figsize=(30, 25), dpi=80)

    Z = hierarchy.linkage(data_two, method='ward', metric='euclidean')
    hierarchy.dendrogram(Z, orientation='right',
                         show_leaf_counts=False,
                         leaf_font_size=15.,
                         labels=data_two.index)

    # 1）创建画布，并设置画布属性
    # 设置切割精确度
    label = cluster.hierarchy.cut_tree(Z, height=heights)
    label = label.reshape(label.size, )

    # for u in keywords:
    #     num = u.encode('utf-8')
    #     # num = u.encode('utf-8')
    #     keywords2.append(num)

    list6.append(keywords)
    list6.append(label)

    list6 = np.array(list6)
    list6 = list6.T

    n = len(list6)

    # 根据不同的阈值返回不同的聚类词
    label2 = list(set(label))
    # global list7
    list7 = [[] for i in range(len(label2))]
    cluster_list = [[] for i in range(len(label2))]

    for i in label2:
        for k in range(n):
            if int(list6[:][k][1]) == int(i):
                list7[label2.index(i)].append(list6[:][k])

    for a in range(len(list7)):
        for j in list7[a]:
            cluster_list[a].append(j[0])
    # num = "number".encode('utf-8')
    # cluster_list = str(cluster_list)
    # cluster_lists = cluster_list.encode("gbk")
    print(cluster_list)
    # 将聚类树形图保存

    picname = "clusters算法".replace(".csv", "")
    # picname = filename.replace(".csv", "")
    picname = picname + "_clusters.png"
    plt.savefig(picname)
    return jsonify(cluster_list=cluster_list)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True,host='0.0.0.0',port=8888)
    # app.run(debug=True,host='192.168.11.220',port=9900)
