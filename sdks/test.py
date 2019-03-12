#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-12 17:02
# @Author  : zpy
# @Software: PyCharm

from app.task import Task

class TestTask(Task):

    def start(self, **kwargs):
        print('instance start', kwargs)
        return 'test'