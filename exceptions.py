#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-07 09:41
# @Author  : zpy
# @Software: PyCharm


class SpiderException(Exception):
    """ 根据不同的 Error code来进行不同的判断,
        重试 3
        默认三次重试，如果三次后还失败 31
        解析出错 5
    """
    DEFAULT = -1
    TASKERROR = 1
    NETERROR = 2
    PARSEERROR = 3


    map_error = {
        DEFAULT: "失败重试",
        TASKERROR: "请检查任务",
        NETERROR: "请检查网络请求",
        PARSEERROR: "请检查解析函数"
    }

    def __init__(self, code, msg=None):
        self.code = code
        self.msg = msg if msg else self.map_error[code]

    def __str__(self):
        return "code: %s, msg: %s" % (self.code, self.msg)

    __repr__ = __str__


class ModelError(Exception):
    pass

if __name__ == '__main__':
    s = SpiderException(SpiderException.DEFAULT, 'wtf')
    raise s