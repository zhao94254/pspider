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


class MongoBackend(BaseBackend):

    def save(self, data):
        log.info("{} {} insert {}".format(str(self.app), self.app.group, len(data)))
        mongo_storage[str(self.app)][self.app.group].insert_many(data)