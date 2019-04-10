#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
# 火灾损失表
# 距离消防站km
x = [3.4, 1.8, 4.6, 2.3, 3.1, 5.5, 0.7, 3.0, 2.6, 4.3, 2.1, 1.1, 6.1, 4.8, 3.8]
# 火灾损失 千元
y = [26.2, 17.8, 31.3, 23.1, 27.5, 36.0, 14.1, 22.3, 19.6, 31.3, 24.0, 17.3, 43.2, 36.4, 26.1]


import matplotlib.pyplot as plt
plt.style.use('ggplot')
## 解决中文字符显示不全
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
plt.scatter(x, y)
plt.xlabel('距离消防站/千米',fontproperties = font)
plt.ylabel("火灾损失/千元",fontproperties = font)
plt.title('火灾损失',fontproperties = font)
plt.show()

