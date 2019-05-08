#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
a = 'hello word'
strinfo = re.compile('word')
b = strinfo.sub('py',a)
print(b)