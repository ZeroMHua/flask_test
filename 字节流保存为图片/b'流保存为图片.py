#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
for X in range(61):
    for Y in range(77):
        url = "http://www.hypathology.com:8092/viewer2/StreamHandler.ashx?SlideID=-1&kfbpath=D:\Slides\hy\KB1902156\KB1902156-1_2019-04-06%2010_36_33.kfb&Zoom=20&FileNum=15&level=15&PositionX={0}&PositionY={1}&TileSize=256&gamma=1.2&contrast=1&light=0&rgbR=0&rgbG=0&rgbB=0".format(X,Y)
# url = "http://www.hypathology.com:8092/viewer2/StreamHandler.ashx?SlideID=-1&kfbpath=D:\Slides\hy\KB1902156\KB1902156-1_2019-04-06%2010_36_33.kfb&Zoom=20&FileNum=15&level=12&PositionX=3&PositionY=4&TileSize=256&gamma=1.2&contrast=1&light=0&rgbR=0&rgbG=0&rgbB=0"
url1 ="http://www.hypathology.com:8092/viewer2/StreamHandler.ashx?SlideID=-1&kfbpath=D:\Slides\hy\KB1902156\KB1902156-2_2019-04-06%2010_37_08.kfb&Zoom=20&FileNum=15&level=15&PositionX=35&PositionY=38&TileSize=256&gamma=1.2&contrast=1&light=0&rgbR=0&rgbG=0&rgbB=0"
response = requests.get(url)
data = response.content
# print(data)
# name = str(X)+str(Y)
file = open('TEST1.jpg', 'wb')
file.write(data)
file.close()