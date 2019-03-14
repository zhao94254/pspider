#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-11 11:58
# @Author  : zpy
# @Software: PyCharm

# 分发任务，控制slave

from flask import Flask, request
from conf.config import redis_client

app = Flask(__name__)

@app.route('/addslave')
def add_slave():
    redis_client.sadd('master|allslaves', request.remote_addr)
    return 'ok'

@app.route('/allslaves')
def all_slaves():
    res = redis_client.smembers('master|allslaves')
    slaves = list(map(lambda x:x.split('|')[1], res))
    slaves.sort()
    return slaves


if __name__ == '__main__':
    app.run(debug=True)
