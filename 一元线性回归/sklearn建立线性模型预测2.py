#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    # 定义自变量x
    x = np.array([[1], [2], [3], [4]], dtype=np.float32)
    # 定义因变量y
    y = np.array([6, 5, 7, 10], dtype=np.float32)
    # 加载scikit-learn的线性模型
    linear = linear_model.LinearRegression()
    # 通过x和y来建立线性模型
    linear.fit(x, y)
    # 查看模型系数β2
    print(linear.coef_)  # [ 1.39999998]
    # 查看模型的截距β1
    print(linear.intercept_)  # 3.5000000596
