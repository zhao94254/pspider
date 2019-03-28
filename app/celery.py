#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-12 15:42
# @Author  : zpy
# @Software: PyCharm

from celery import Celery
from kombu import Queue, Exchange
from conf.config import celery_broker
from plogger import get_logger


log = get_logger('celery_init')

capp = Celery(
    'app',
    broker=celery_broker
)

# 保证任务是可靠的执行了
capp.conf.update(CELERY_REJECT_ON_WORKER_LOST=True, CELERY_ACKS_LATE=True)

def init_sdks():
    from app.register import _all_sdk_
    from app import tasks
    queues = []
    for s in _all_sdk_:
        s.app = capp
        name = s.__str__()
        log.info("load %s", name)
        tasks.__dict__[name] =  s.ptask(name, rate_limit='10/m')
        queues.append(Queue(name, exchange=Exchange(name, type='direct'), routing_key=name))

    capp.conf.update(
        CELERY_QUEUES=queues
    )
    capp.conf.update(CELERY_INCLUDE=['app.tasks'])

init_sdks()