#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import numpy as np
from scipy.stats import kstest, norm
import matplotlib.pyplot as plt
ls = [1,2,3,4,5,6,7,6,5,4,3,2,1]
ls = np.array(ls)
ls.sort()
n = len(ls)

# x中第一个为统计量，第二个为P值
x=kstest(ls, 'norm')
print(x)
y_list = [float(i) / n for i in range(1, n + 1)] # 求观察累积概率y_list

x_list = [norm.ppf(ele) for ele in y_list] # 用累积概率求分位数值x_list

plt.plot(x_list, y_list)

plt.savefig("QQ正态分布.png")