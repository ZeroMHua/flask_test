#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:hua
from flask import Blueprint, render_template, redirect

user = Blueprint('user',__name__)

@user.route('/index',method=['GET'])
def index():
    return ('user/index')

@user.route('/add')
def add():
    return 'user_add'

@user.route('/show')
def show():
    return 'user_show'