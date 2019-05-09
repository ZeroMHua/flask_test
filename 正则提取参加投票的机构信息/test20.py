#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
data = "nmnm你好啊，你好滚滚滚？kkkj123"
p = '[^a-zA-Z0-9]'
# p = '[\u4e00-\u9fa5]+'
result = re.findall(p, data)
s1 = "".join(result)
print(s1)