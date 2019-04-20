#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
"""
https://www.cnblogs.com/jasonfreak/p/5441512.html
包	   方法	      说明
numpy	array	  创造一组数
numpy.random	  normal	创造一组服从正态分布的定量数
numpy.random	  randint	创造一组服从均匀分布的定性数
numpy	mean	  计算均值
numpy	median	  计算中位数
scipy.stats	mode	计算众数
numpy	ptp	      计算极差
numpy	var	      计算方差
numpy	std	      计算标准差
numpy	cov	      计算协方差
numpy	corrcoef	计算相关系数
 
"""
from numpy import array, mean, median, ptp, var, std
from numpy.random import normal, randint
from scipy.stats import mode

# 使用List来创造一组数据
data = [1, 2, 3, 4, 5, 6, 7]
# 使用ndarray来创造一组数据
data = array(data)
# 创造一组服从正态分布的定量数据
data1 = normal(0, 10, size=10)
# print(data1)
# 创造一组服从均匀分布的定性数据
data2 = randint(0, 10, size=10)
# print(data2)
# print(median(data))
# 中位数
# 计算均值
data_mid = mean(data)
# print(data_mid)
# 计算中位数
x, y = mode(data)
# print(x[0])

# 极差
print(ptp(data2))
# 方差
var(data)
# 标准差
std(data)
# 变异系数
mean(data) / std(data)
