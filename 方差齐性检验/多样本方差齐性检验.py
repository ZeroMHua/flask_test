#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from scipy import stats

list1 = [x for x in range(5)]
list2 = [y for y in range(10,20)]
list3 = [u for u in range(30,40)]
list4 = ["a","b","c","d","e"]
data = stats.levene(list1,list2,list3)
print(data)