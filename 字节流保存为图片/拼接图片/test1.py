#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import PIL.Image as Image
import os, sys
mw = 256 # 图片大小
toImage = Image.new('RGB', (25171, 25171))#构造图片的宽和高，如果图片不能填充完全会
#出现黑色区域
for y in range(31):#0-46
        fname = "16_%d.jpg" %(y)
        fromImage = Image.open(fname)
        toImage.paste(fromImage, (16 * mw, y * mw))
toImage.save('./何萍.jpg')
