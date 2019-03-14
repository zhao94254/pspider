#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-14 10:33
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
        self.save(list(spider.result['job'].export_dict()))

if __name__ == '__main__':
    l = LagouTask(tasks=['https://www.lagou.com/zhaopin/Python/12'], group='20190314')
    l.start()