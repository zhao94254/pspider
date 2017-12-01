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


def get_sort():
    d = danmu.aggregate([{"$group": {"_id": "$rid", "count": {"$sum": 1}}}, {"$sort": SON([("count", -1)])}])
    for i in d:
        print(i)


get_sort()
