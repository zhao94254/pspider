#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-12 17:02
# @Author  : zpy
# @Software: PyCharm

from app.task import Task
from example.testspider import LagouSpider

class TestTask(Task):

    def start(self, **kwargs):
        print('instance start', kwargs)
        return 'test'

class LagouTask(Task):

    def start(self):
        spider = LagouSpider()
        spider.tasks = self.tasks
        spider.start()
        for d in spider.result['job'].export_sql('test.test'):
            print(d)