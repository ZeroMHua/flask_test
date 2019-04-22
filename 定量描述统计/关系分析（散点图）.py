#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from matplotlib import pyplot

#绘制散点图
def drawScatter(heights, weights):
    #创建散点图
    #第一个参数为点的横坐标
    #第二个参数为点的纵坐标
    pyplot.scatter(heights, weights)
    pyplot.xlabel('Heights')
    pyplot.ylabel('Weights')
    pyplot.title('Heights & Weights Of Male Students')
    pyplot.show()
heights = [heights for heights in range(10)]
weights = [weights for weights in range(10,20)]
drawScatter(heights, weights)