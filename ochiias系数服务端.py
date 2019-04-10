# -*- coding:utf-8 -*-
# Author:hua
from copy import deepcopy
from flask import Flask, jsonify
from flask import request
from numpy import math
from pandas import DataFrame
from scipy.stats import mode
import numpy as np
import json

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    return "ochiias算法"

@app.route('/ochiias', methods=['GET', 'POST'])
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
    # keywords = keywords.columns
    # keywords = list(keywords)

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
            c = [i, k]

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
            ochiia = sum_two / (sqrt_i * sqrt_k)
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
    data_save = DataFrame(data_save, index=keywords, columns=keywords)

    for ii in keywords:
        # ii = ii.encode("gbk")
        # print(ii)

        for kk in keywords:
            ds = data_save.loc[ii, kk]
            nn = 1
            if nn <= n:
                # dic = {"name":ii,kk:ds}
                # kk = kk.decode("gbk")
                dic = {kk: ds}

                list4.append(dic)

    # 组合成java想要的输出格式
    global ff
    ff = [list4[i:i + n] for i in range(0, len(list4), n)]
    # 添加name这个key
    for i in range(n):
        dic4 = {"name": keywords[i]}
        ff[i].append(dic4)

    for k in range(len(ff)):
        for i in ff[k]:
            for i, j in i.items():
                total_dic[i] = j
        t = deepcopy(total_dic)

        t1 = json.dumps(t)
        # 使用t2,可以正常显示中文
        t2 = eval(t1)
        # print(t2)

        # t1 = t1.decode("unicode-escape")

        # print type(t1)

        # print t1
        data_list.append(t2)
    # data_list = str(data_list)
    # data_list = data_list.decode("unicode-escape")
    # data_list = data_list.replace("u'", "")
    # data_list = data_list.replace("'", "")
    # data_list = data_list.encode('utf-8')
    print(data_list)

    # return data_list
    return jsonify(data_list=data_list)

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0',port=8888)
    app.run(debug=True,host='192.168.11.220',port=9900)

