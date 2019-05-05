#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests

for X in range(37):
    for Y in range(61):
        url = "http://www.hypathology.com:8092/viewer2/StreamHandler.ashx?SlideID=-1&kfbpath=D:\Slides\hy\KB1902890\KB1902890-1_2019-05-05%2009_26_48.kfb&Zoom=20&FileNum=14&level=14&PositionX={0}&PositionY={1}&TileSize=256&gamma=1.2&contrast=1&light=0&rgbR=0&rgbG=0&rgbB=0".format(
            X, Y)
        response = requests.get(url)
        data = response.content
        # print(data)
        name = str(X)+"_" + str(Y)
        print(X)
        file = open('./何萍/{}.jpg'.format(name), 'wb')
        file.write(data)
        file.close()
