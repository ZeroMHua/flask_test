#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import numpy

import matplotlib.pyplot as plt
from scipy.stats import norm

input_list=numpy.random.normal(size=100) # 生成随机数, 这里生成正态分布随机数

input_list.sort() #将input_list从小达到排序

n = len(input_list)

y_list = [float(i) / n for i in range(1, n + 1)] # 求观察累积概率y_list

x_list = [norm.ppf(ele) for ele in y_list] # 用累积概率求分位数值x_list

plt.plot(x_list, y_list)

plt.show()