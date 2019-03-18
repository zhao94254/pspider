#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-14 18:49
# @Author  : zpy
# @Software: PyCharm

# todo 完善

from conf.config import mongo_storage
from plogger import get_logger

log = get_logger("storage")

class BaseBackend(object):

    def __init__(self, app):
        self.app = app

    def pre_check(self):
        """
        检查传入的配置、参数
        :return:
        """
        pass


class MongoBackend(BaseBackend):

    def save(self, data): # todo 这里应该传入数据还是？
        log.info("{} {} insert {}".format(str(self.app), self.app.group, len(data)))
        mongo_storage[str(self.app)][self.app.group].insert_many(data)


class MysqlBackend(BaseBackend):

    def save(self, data, sql):
        pass


class RedisBackend(BaseBackend):

    def save(self, data):
        pass

def dispatch(conf):
    """
    根据配置指到不同的类
    :param conf:
    :return:
    """
    pass