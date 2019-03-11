#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-06 17:18
# @Author  : zpy
# @Software: PyCharm

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