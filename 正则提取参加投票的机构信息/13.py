#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
import re

# 测试文本
test = '<h1>hello 你好, world 世界</h1>'

# 中文匹配正则
chinese_pattern = '[\u4e00-\u9fa5]+'
says = re.findall(chinese_pattern, test)
print(says)