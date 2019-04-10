#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# 火灾损失表
# 距离消防站km
x = [3.4, 1.8, 4.6, 2.3, 3.1, 5.5, 0.7, 3.0, 2.6, 4.3, 2.1, 1.1, 6.1, 4.8, 3.8]
# 火灾损失 千元
y = [26.2, 17.8, 31.3, 23.1, 27.5, 36.0, 14.1, 22.3, 19.6, 31.3, 24.0, 17.3, 43.2, 36.4, 26.1]

import numpy as np
from sklearn.linear_model import LinearRegression

x_in = np.array(x).reshape(-1, 1)
y_in = np.array(y).reshape(-1, 1)
lreg = LinearRegression()
lreg.fit(x_in, y_in)
y_prd = lreg.predict(x_in)


# 统计量参数
def get_lr_stats(x, y, model):
    message0 = '一元线性回归方程为: ' + '\ty' + '=' + str(model.intercept_[0]) + ' + ' + str(model.coef_[0][0]) + '*x'
    from scipy import stats
    n = len(x)
    y_prd = model.predict(x)
    Regression = sum((y_prd - np.mean(y)) ** 2)  # 回归
    Residual = sum((y - y_prd) ** 2)  # 残差
    R_square = Regression / (Regression + Residual)  # 相关性系数R^2
    F = (Regression / 1) / (Residual / (n - 2))  # F 分布
    pf = stats.f.sf(F, 1, n - 2)
    message1 = ('相关系数(R^2)： ' + str(R_square[0]) + '；' + '\n' +
                '回归分析(SSR)： ' + str(Regression[0]) + '；' + '\t残差(SSE)： ' + str(Residual[0]) + '；' + '\n' +
                '           F ： ' + str(F[0]) + '；' + '\t' + 'pf ： ' + str(pf[0]))
    ## T
    L_xx = n * np.var(x)
    sigma = np.sqrt(Residual / n)
    t = model.coef_ * np.sqrt(L_xx) / sigma
    pt = stats.t.sf(t, n - 2)
    message2 = '           t ： ' + str(t[0][0]) + '；' + '\t' + 'pt ： ' + str(pt[0][0])
    return print(message0 + '\n' + message1 + '\n' + message2)


get_lr_stats(x_in, y_in, lreg)
