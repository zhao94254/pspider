#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-11 11:58
# @Author  : zpy
# @Software: PyCharm

# 分发任务，控制subordinate

from flask import Flask, request
from conf.config import redis_client

app = Flask(__name__)

@app.route('/addsubordinate')
def add_subordinate():
    redis_client.sadd('main|allsubordinates', request.remote_addr)
    return 'ok'

@app.route('/allsubordinates')
def all_subordinates():
    res = redis_client.smembers('main|allsubordinates')
    subordinates = list(map(lambda x:x.split('|')[1], res))
    subordinates.sort()
    return subordinates


if __name__ == '__main__':
    app.run(debug=True)
