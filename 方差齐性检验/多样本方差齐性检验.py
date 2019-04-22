#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from scipy import stats

list1 = [x for x in range(10)]
list2 = [y for y in range(10,20)]
list3 = [u for u in range(30,40)]
data = stats.levene(list1,list2,list3)
print(data)