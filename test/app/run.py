#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Flask, jsonify
from flask import request
from scipy.stats import ttest_ind

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)