#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import numpy as np
import pandas as pd
df=pd.DataFrame({"one":np.random.randn(4),"two":np.linspace(1,4,4),"three":["zhangsan","lisi",999.99,1]})
print(df)
df1 = str(df)


file = open('TEST2.txt', 'a')
file.write(df1)
file.close()
# ax = df.plot()
# fig = ax.get_figure()
# fig.savefig('fig.png')
# # fig.show()