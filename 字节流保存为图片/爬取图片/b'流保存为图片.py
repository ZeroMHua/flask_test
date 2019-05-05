#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests

for X in range(45):
    for Y in range(81):
        url = "http://www.hypathology.com:8092/viewer2/StreamHandler.ashx?SlideID=-1&kfbpath=H:\Slides\KB184432\KB184432-2_2018-12-01%2015_25_00.kfb&Zoom=20&FileNum=15&level=15&PositionX={0}&PositionY={1}&TileSize=256&gamma=1.2&contrast=1&light=0&rgbR=0&rgbG=0&rgbB=0".format(
            X, Y)

        response = requests.get(url)
        data = response.content
        # print(data)
        name = str(X)+"_" + str(Y)
        print(X)
        file = open('./林钰银/{}.jpg'.format(name), 'wb')
        file.write(data)
        file.close()
