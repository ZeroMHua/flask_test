#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import numpy as np
from scipy.stats import normaltest
ls = [1,2,3,4,5,6,7,6,5,4,3,2,1]
# ls = [x for x in range(10)]
ls = np.array(ls)
x=normaltest(ls, axis=None)
print(x)
