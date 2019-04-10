#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=10)
from sklearn import linear_model        #表示，可以调用sklearn中的linear_model模块进行线性回归。
import numpy as np
X = [[6], [8], [10], [14], [18]]
y = [[7], [9], [13], [17.5], [18]]
model = linear_model.LinearRegression()
model.fit(X, y)
q=model.intercept_  #截距
print(q)
# display(model.coef_)  #线性模型的系数
r = model.coef_  #线性模型的系数
print(r)
a = model.predict([[5]])
print(a)
# a[0][0]
print("预测一张12英寸匹萨价格：{:.2f}".format(model.predict([[5]])[0][0]))