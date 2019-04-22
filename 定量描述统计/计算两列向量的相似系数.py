#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import pandas as pd
d = pd.DataFrame([range(1,8)],range(2,9))
d.corr(method="pearson")#计算相关系数
s1 = d.loc[0]
s2 = d.loc[1]
p= s1.corr(s2,method="pearson")
print(p)