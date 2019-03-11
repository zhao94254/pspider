#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-07 17:16
# @Author  : zpy
# @Software: PyCharm

# 定义数据结构，对结果进行检查

from exceptions import ModelError
from collections import OrderedDict
from copy import deepcopy, copy
import csv

class SDict(OrderedDict):

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)


class BaseModel:

    def __init__(self, mds):
        """
        :param mds:[(sp, int), (ps, str)]
        """
        self.mds = mds
        self.mds_map = {}
        self.res = SDict()
        self.check()
        self.buffer = []

    def _check_mds(self):
        for i in self.mds:
            if len(i) != 2:
                raise ModelError
            self.mds_map[i[0]] = i[1]
            if isinstance('str', i[1]):
                self.res[i[0]] = "NULL"
            elif isinstance(1, i[1]):
                self.res[i[0]] = -1
            elif isinstance(1.0, i[1]):
                self.res[i[0]] = -1.0

    def check(self):
        self._check_mds()

    def export_sql(self, table):
        """
        导出sql
        :param table:
        :return:
        """
        fmtsql = "insert into {table} {keys} values({values})".format(table=table, keys=','.join(self.res.keys()),
                                                             values='%s,' * len(self.res))

        for data in self.buffer:
            yield fmtsql % tuple(data.values())

    def export_csv(self):
        """
        导出csv 格式
        :return:
        """
        yield ",".join(self.res.keys())
        for data in self.buffer:
            yield ",".join(map(str, data.values()))

    def export_csvfile(self, filepath):
        """
        导出csv文件
        :param filepath:
        :return:
        """
        with open(filepath, 'w') as f:
            csvw = csv.writer(f)
            csvw.writerow(self.res.keys())
            for d in self.buffer:
                csvw.writerow(d.values())

    def export_tuple(self):
        """
        导出元组
        :return:
        """
        for data in self.buffer:
            yield tuple(data.values())

    def save(self):
        """
        将数据先缓存到model 实例中
        :return:
        """
        self.buffer.append(copy(self.res))

if __name__ == '__main__':
    # s = SDict()
    # s.d = 2
    # print(s)

    tmodel = BaseModel([('name', str), ('age', int)])
    tmodel.res.ks = 2
    print(tmodel.res)
    tmodel.save()

    for s in tmodel.export_sql('test'):
        print(s)

    for s in tmodel.export_csv():
        print(s)

    tmodel.export_csvfile('/Users/mioji/Desktop/newpy/test.csv')