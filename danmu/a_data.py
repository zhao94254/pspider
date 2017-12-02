#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/1 下午7:10
# @Author  : zpy
# @Software: PyCharm


from pymongo import MongoClient
from bson import SON

client = MongoClient('mongodb://localhost:27017/')
db = client.crawl
danmu = db.danmu


def get_sort(s):
    """根据不同的字段，按照不同类型统计排行
    主要是rid 主播房间 uid 用户 level 等
    """
    d = danmu.aggregate([{"$group": {"_id": "${}".format(s), "count": {"$sum": 1}}},
                         {"$sort": SON([("count", -1)])}], allowDiskUse=True) # allowDiskUse 启动这个，防止内存不够用
    for i, j in enumerate(d):
        if i == 50:
            break
        print(j)
    print('end')

if __name__ == '__main__':
    print('房间排名','-' * 50)
    get_sort('rid')
    print('用户','-' * 50)
    get_sort('uid')
    print('等级','-' * 50)
    get_sort('level')
