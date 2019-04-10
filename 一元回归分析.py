#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
# %matplotlib inline

x = [13854,12213,11009,10655,9503] #程序员工资，顺序为北京，上海，杭州，深圳，广州
x = np.reshape(x,newshape=(5,1)) / 10000.0
y =  [21332, 20162, 19138, 18621, 18016] #算法工程师，顺序和上面一致
y = np.reshape(y,newshape=(5,1)) / 10000.0
# 调用模型
lr = LinearRegression()
# 训练模型
lr.fit(x,y)
# 计算R平方
print(lr.score(x,y))
# 计算y_hat
y_hat = lr.predict(x)
# 打印出图
plt.scatter(x,y)
plt.plot(x, y_hat)


