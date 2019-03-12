#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-06 17:36
# @Author  : zpy
# @Software: PyCharm

import logging
from logging.handlers import RotatingFileHandler
import functools
import inspect
from datetime import datetime
from collections import defaultdict
import os
from config import LOGPATH as log_path

class NamedRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename):
        super(NamedRotatingFileHandler, self).__init__(
            filename=os.path.join(log_path, "{0}.log".format(filename)),
            maxBytes=100 * 1024 * 1024,
            backupCount=2
        )

def get_logger(logger_name):
    """
    初始化 logger get 可以获取到，为单例模式
    """
    if not os.path.exists(log_path):
        os.makedirs(log_path)
        os.mkdir(log_path)

    # getLogger 为单例模式
    service_platform_logger = logging.getLogger(logger_name)
    service_platform_logger.setLevel(logging.DEBUG)
    datefmt = "%Y-%m-%d %H:%M:%S"
    file_log_format = "%(asctime)-15s %(threadName)s %(filename)s:%(lineno)d %(levelname)s:        %(message)s"
    formtter = logging.Formatter(file_log_format, datefmt)

    # handler 存在的判定
    if not service_platform_logger.handlers:
        # rotating file logger
        file_handle = NamedRotatingFileHandler(logger_name)
        file_handle.setFormatter(formtter)
        service_platform_logger.addHandler(file_handle)
        steam_handler = logging.StreamHandler()
        service_platform_logger.addHandler(steam_handler)

    return service_platform_logger

func_count_dict = defaultdict(int)
time_logger = get_logger('func_time_logger')


def func_time_logger(fun):
    @functools.wraps(fun)
    def logging(*args, **kw):
        try:
            func_file = inspect.getfile(fun)
        except Exception:
            func_file = ''
        func_name = fun.__name__
        func_key = (func_file, func_name)
        func_count_dict[func_key] += 1
        begin = datetime.now()
        result = fun(*args, **kw)
        end = datetime.now()
        time_logger.debug('file={} func={} costtime={} times={} args={} kwargs={}'.format(
            func_file, func_name, end - begin, func_count_dict[func_key], args, kw
        ))
        func_count_dict[func_key] -= 1
        return result

    return logging