#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import pandas as pd
import numpy as np
data = pd.read_csv("ceshi.csv",encoding="gbk")
age = data["年龄"]
age = np.array(age)
print(type(age))