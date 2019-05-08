#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import re
with open("test2.txt","r",encoding="utf-8") as f:
    s11 = f.read()
# print(s11)
s1=s11.strip()
s2 = s1.replace(">","")
s3 = s2.replace("<","")
s4 = s2.replace("=","")
s5 = s4.replace("=","")
s6 = re.sub('[<>?;($#&":\-\'.//!}{)_]+','',s5)
s7=s6.replace('<>< ="-:','')
print(s7)
file = open('test3.txt', 'wb')
file.write(str(s7).encode("utf-8"))
file.close()