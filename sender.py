#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-12 16:18
# @Author  : zpy
# @Software: PyCharm

from app.celery import capp
from app.task import Task
from app.sdks import _all_sdk_



if __name__ == '__main__':

    test = _all_sdk_[0]
    print(test.app)
    test.send('skr')