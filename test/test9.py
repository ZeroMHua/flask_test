#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

reg = linear_model.LinearRegression()
reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])

LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None,
                 normalize=False)
print(reg.coef_)