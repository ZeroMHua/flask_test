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

print('残差平方和:{:.2f}'.format(np.mean((model.predict(X) - y) ** 2)))

"""
有些度量方法可以用来评估预测效果，我们用R方（r-squared）评估匹萨价格预测的效果。R方也叫 
确定系数（coefficient of determination），表示模型对现实数据拟合的程度。计算R方的方法有几 
种。一元线性回归中R方等于皮尔逊积矩相关系数（Pearson product moment correlation coefficient 
或Pearson’s r）的平方
"""
# 测试集
X_test = [[8], [9], [11], [16], [12]]
y_test = [[11], [8.5], [15], [18], [11]]
model = linear_model.LinearRegression()
model.fit(X, y)
R = model.score(X_test, y_test)
print(R)