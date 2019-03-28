#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-12 17:02
# @Author  : zpy
# @Software: PyCharm

from app.task import Task
from example.testspider import LagouSpider
from example.zhihuspider import BihuSpider
from conf.config import redis_client, mongo_storage
import time
from plogger import get_logger

log  = get_logger('testsdks')

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


class BihuTask(Task):

    def create_task(self, data):
        for k in data:
            if redis_client.sadd('bihuset',k['url_token']):
                redis_client.lpush('bihutask',k['url_token'] )
        log.info('now task number {} {}'.format(redis_client.llen('bihutask'), redis_client.scard('bihuset')))

    def execute(self):

        sp = BihuSpider() # 按照用户为粒度
        sp.tasks = 'https://www.zhihu.com/api/v4/members/{}/followees?offset=0&limit=20'.format(self.tasks)
        sp.start()
        mongo_storage['dev']['bihu'].insert({'name':self.tasks, 'followee': sp.result['data']['data']})
        self.create_task(sp.result['data']['data'])
        for _ in range(100):
            time.sleep(3)
            if sp.result['data']['next_page']:
                sp.tasks = sp.result['data']['next_page']
                sp.start()
                mongo_storage['dev']['bihu'].insert({'name': self.tasks, 'followee': sp.result['data']['data']})
                self.create_task(sp.result['data']['data'])
            else:
                break


if __name__ == '__main__':
    BihuTask(tasks='', group='test', source='ptest').execute()