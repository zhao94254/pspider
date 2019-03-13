#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-12 16:18
# @Author  : zpy
# @Software: PyCharm

from app.celery import capp
from app.task import Task
from app.register import _all_sdk_



if __name__ == '__main__':
    # for i in range(10):
    test = _all_sdk_[1]
    test.send(tasks=['https://www.lagou.com/zhaopin/Python/1'])