#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-11 22:41
# @Author  : zpy
# @Software: PyCharm


from app.task import Task

class FakeApp(object):

    @staticmethod
    def task(bind=True, **kwargs):
        def skr(func, **kws):
            def inner(**kws):
                print('start', kwargs)
                res = func(**kws)
                print('end')
                return res
            return inner
        return skr

class TestTask(Task):

    def start(self, **kwargs):
        print('instance start', kwargs)
        return 'test'


app = FakeApp()

@app.task(bind=True, skr='skr')
def testskr1(**kwargs):
    print("--- testskr")
    _test = TestTask()
    return _test.start(**kwargs)



if __name__ == '__main__':
    # TestTask.app = FakeApp()
    # TestTask().ptask(skr='skr')


    print(testskr1(s=2))