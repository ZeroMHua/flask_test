#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from sklearn import linear_model
from sklearn.linear_model import BayesianRidge

X = [[0., 0.], [1., 1.], [2., 2.], [3., 3.]]
Y = [0., 1., 2., 3.]
reg = linear_model.BayesianRidge()
reg.fit(X, Y)
BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, compute_score=False, copy_X=True,
              fit_intercept=True, lambda_1=1e-06, lambda_2=1e-06, n_iter=300,
              normalize=False, tol=0.001, verbose=False)
xx = reg.predict ([[1, 0.]])
print(xx)