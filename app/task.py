#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-11 22:25
# @Author  : zpy
# @Software: PyCharm

from plogger import get_logger

log = get_logger('core_task')

class Task(object):
    """
    在 celery 上封装一层， 任务的调度，执行，分发都会依靠这里来做
    """

    app = None

    def __init__(self,**kwargs):
        self.tasks = kwargs['tasks']
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
    def send(cls, tasks):
        name = cls.__str__()
        log.info("%s send task", name)
        return cls.app.send_task(name, kwargs={'tasks':tasks}, queue=name, routing_key=name)

    def start(self):
        pass

    def execute(self):
        pass

    @classmethod
    def __str__(cls):
        return cls.__name__