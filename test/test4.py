#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
import requests
url = "https://gateio.co/trade/EOS_USDT"
response = requests.get(url)
data = response.content.decode("utf-8")
print(data)