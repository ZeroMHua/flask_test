#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import PIL.Image as Image
import os, sys
mw = 256 # 图片大小
toImage = Image.new('RGB', (25171, 11802))
for x in range(45):
    for y in range(81):
        fname = "%d_%d.jpg" %(x,y)
        fromImage = Image.open(fname)
        toImage.paste(fromImage, (x * mw, y * mw))
toImage.save('./image2.jpg')
