#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import numpy as np
from scipy import stats
np.random.seed(7654567)  # 保证每次运行都会得到相同结果
# 均值为5，方差为10
rvs = stats.norm.rvs(loc=5, scale=10, size=(50,2))
# 检验两列数的均值与1和2的差异是否显著
result = stats.ttest_1samp(rvs, [1, 2])
"""
分别显示两列数的t统计量和p值。由p值分别为0.042和0.018，当p值小于0.05时，
认为差异显著，即第一列数的均值不等于1，第二列数的均值不等于2。"""
x,y = result
print(x)
print(y)