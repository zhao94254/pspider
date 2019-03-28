#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-11 22:25
# @Author  : zpy
# @Software: PyCharm

from plogger import get_logger
from conf.config import redis_client
from backend.storage import MongoBackend

log = get_logger('core_task')

# 1个sdk -> n个 source -> n个group

# todo config 子task粒度的（celery配置） 具体一批任务粒度的（结果配置、备份配置等）

class Task(object):
    """
    在 celery 上封装一层， 任务的调度，执行，分发都会依靠这里来做
    """

    app = None

    def __init__(self,**kwargs): # todo 接口设计
        self.tasks = kwargs['tasks']
        self.group = kwargs['group']
        self.source = kwargs['source']
        self.code = -1
        log.info(('init', kwargs))

    def set_config(self):
        pass

    @classmethod
    def clstasks(cls, name, **kwargs):
        return cls.app.task(bind=True,name=name, **kwargs)

    @classmethod
    def ptask(cls, name, **kwargs):
        @cls.clstasks(name=name, **kwargs)
        def _instance(*args, **kwargs):
            cls(**kwargs).start()
        return _instance

    @classmethod
    def send(cls, tasks: list, group: str, source: str):
        name = cls.__str__()
        log.info("%s send task", name)
        return cls.app.send_task(name, kwargs={'tasks':tasks, 'group':group, 'source':source}, queue=name, routing_key=name)

    def start(self):
        self.log_task()
        self.execute()
        self.log_task()

    def execute(self):
        pass

    def save(self, data):
        return MongoBackend(self).save(data)

    def log_task(self):
        """
        记录任务执行情况
        :return:
        """
        redis_client.incr("{}|{}".format(str(self), self.code), 1)
        log.info("{}|{}".format(str(self), self.code))

    @classmethod
    def __str__(cls):
        return "{}_{}".format(cls.__module__, cls.__name__).replace('.', '_')

    __repr__ = __str__