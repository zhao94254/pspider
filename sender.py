#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-12 16:18
# @Author  : zpy
# @Software: PyCharm

from app.celery import capp
from app.task import Task
from app.register import _all_sdk_
from conf.config import redis_client
from functools import partial
from apscheduler.schedulers.blocking import BlockingScheduler
schedule = BlockingScheduler()

def bihusender():
    test = _all_sdk_[-1]
    t = redis_client.rpop('bihutask')
    test.send(tasks=t.decode(), source='follow', group='20190327')

schedule.add_job(bihusender,'cron', second='*/10', max_instances=1)



if __name__ == '__main__':
    # for i in range(10):
    schedule.start()