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


"""
方法二：
scipy.stats.normaltest
normaltest 也是专门做正态性检验的模块
scipy.stats.normaltest(a, axis=0, nan_policy=’propagate’)
这里的三个参数都有必要看一下：
a：待检验的数据
axis：默认为0，表示在0轴上检验，即对数据的每一行做正态性检验，我们可以设置为 axis=None 来对整个数据做检验
nan_policy：当输入的数据中有空值时的处理办法。默认为 ‘propagate’，返回空值；设置为 ‘raise’ 时，抛出错误；设置为 ‘omit’ 时，在计算中忽略空值。

import numpy as np
from scipy.stats import normaltest
x = np.random.randn(10, 20)
xx = normaltest(x, axis=None)
print(xx)
# NormaltestResult(statistic=0.3582062593239369, pvalue=0.83601967652440512)
# 结果返回两个值：statistic → D值，pvalue → P值
# p值大于0.05，很可能为正态分布

"""
import numpy as np
from scipy.stats import normaltest
x = np.random.randn(10, 20)
xx,p = normaltest(x, axis=None)
if p>0.05:
    print(222)


