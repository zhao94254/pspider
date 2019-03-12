#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-11 22:25
# @Author  : zpy
# @Software: PyCharm


class Task(object):
    """
    在 celery 上封装一层， 任务的调度，执行，分发都会依靠这里来做
    """

    app = None

    def __init__(self, **kwargs):
        pass

    def set_config(self):
        pass

    @classmethod
    def clstasks(cls, **kwargs):
        return cls.app.task(bind=True, **kwargs)

    @classmethod
    def ptask(cls, **kwargs):
        @cls.clstasks(**kwargs)
        def _instance(**kwargs):
            cls(**kwargs).start()
        return _instance

    def start(self):
        pass

    def execute(self):
        pass

    @classmethod
    def __str__(cls):
        return cls.__module__ + cls.__name__