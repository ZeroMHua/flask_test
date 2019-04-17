#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import pandas as pd
data = pd.read_csv("ceshi.csv",encoding="gbk")
print(data["年龄"])