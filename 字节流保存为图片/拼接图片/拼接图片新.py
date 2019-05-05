#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import PIL.Image as Image
import os, sys
mw = 256 # 图片大小
toImage = Image.new('RGB', (25171, 11802))#构造图片的宽和高，如果图片不能填充完全会
#出现黑色区域
for x in range(76):#0-46
    for y in range(101):#0-98
        fname = "%d_%d.jpg" %(x,y)
        fromImage = Image.open(fname)
        toImage.paste(fromImage, (x * mw, y * mw))
toImage.save('./image2.jpg')