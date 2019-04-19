#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
"""
方法一：
scipy.stats.kstest
kstest 是一个很强大的检验模块，除了正态性检验，还能检验 scipy.stats 中的其他数据分布类型
kstest(rvs, cdf, args=(), N=20, alternative=’two_sided’, mode=’approx’, **kwds)
对于正态性检验，我们只需要手动设置三个参数即可：
rvs：待检验的数据
cdf：检验方法，这里我们设置为‘norm’，即正态性检验
alternative：默认为双尾检验，可以设置为‘less’或‘greater’作单尾检验

import numpy as np
from scipy.stats import kstest
import matplotlib.pyplot as plt
ls = [1,2,3,4,5,6,7,6,5,4,3,2,1]
ls = np.array(ls)
ls.sort()
x=kstest(ls, 'norm')
print(x)
"""
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


