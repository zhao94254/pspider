#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-06 17:18
# @Author  : zpy
# @Software: PyCharm

import pymysql
from pymysql import cursors

def get_local_ip():
    import socket
    res = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        res = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    return res

class Mysql:
    def __init__(self, stream=False, **kw): #  MySQLdb.cursors.SSCursor 流式游标
        if stream == True:
            self._connect = pymysql.connect(cursorclass = cursors.SSCursor, **kw)
        else:
            self._connect = pymysql.connect(**kw)
    def __enter__(self):

        self.cursor = self._connect.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):

        self._connect.commit()
        self.cursor.close()
        self._connect.close()