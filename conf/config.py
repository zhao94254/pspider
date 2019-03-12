#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-12 15:44
# @Author  : zpy
# @Software: PyCharm

dev = True

if dev:
    from conf.dev_config import *
else:
    from conf.product_config import *