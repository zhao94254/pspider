#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-06 17:19
# @Author  : zpy
# @Software: PyCharm

import abc
from abc import ABCMeta
from spider.plogger import get_logger, func_time_logger
from exceptions import SpiderException
from requests.exceptions import Timeout, ConnectionError
from collections import deque
from spider.prequest import Msession

log = get_logger('pspider')

# todo v1 完成
# 请求解析初版
# 先不考虑链式请求

class Pspider(metaclass=ABCMeta):

    def __init__(self):
        self.result = {}
        self.session = None

    @abc.abstractmethod
    def task(self):
        pass

    @abc.abstractmethod
    def req_resp(self):
        pass

    def start(self):
        for worker in self.req_resp():
            worker.pspider = self
            worker.run()

    @property
    def brower(self):
        if self.session is None:
            self.session = Msession()
        return self.session

    def reset_brower(self):
        """
        重置session
        :return:
        """
        log.info("重置Session")
        self.brower.close()
        self.session = None


def req(retry=3, proxy=False, timeout=30, concurren=1):
    """ 通过装饰器来给出可选的配置。 """
    def call(func):
        req = ReqParse(func, retry=retry, proxy=proxy, timeout=timeout, concurren=concurren)
        return req
    return call



class ReqParse:
    """ 请求和解析处理包在此函数里做

    """
    insert = None
    def __init__(self, func, retry=3, proxy=False,timeout=30, concurren=1):
        """
        :param func: 请求&解析
        :param retry: 重试次数
        :param proxy: 是否使用代理
        :param timeout: 超时
        :param concurren: 并发
        """

        self._req_func = func
        self.retry = retry
        self.proxy = proxy
        self.timeout = timeout
        self.concurren = concurren
        self.session = None
        self.pspider = None

    def parse_func(self):
        """ 放置请求的函数和处理返回的函数
        self._req_func: {
            "request":{
                "url": http://xxxx,
                "header": xxx,
                ...
            }
            "response":{
                "handler": xxx,  # handler最后返回 dict list（一般用在列表页） str
            }
        }
        """
        r = self._req_func()
        if 'request' in r and 'response' in r:
            _req = r['request']
            _resp = r['response']
            if 'url' not in _req or 'handler' not in _resp or 'result_tag' not in _resp: # 添加result_tag
                raise SpiderException(SpiderException.TASKERROR)
            else:
                self.result_tag = _resp['result_tag']
                self.urls = _req['url']
                self.kw = _req['kw'] if 'kw' in _req else {}
                self.handler = func_time_logger(_resp['handler'])
                self.method = 'get' if 'methods' not in _req else _req['methods']
                if self.method == 'post':
                    if 'postdata' in _req:
                        self.postdata = _req['postdata']
                    else:
                        raise SpiderException(SpiderException.TASKERROR, '如果无post的数据请给一个空字符串。')
        else:
            raise SpiderException(SpiderException.TASKERROR)

    @func_time_logger
    def _spider_run(self, url):
        """ 执行真正的请求。控制代理， 超时等设置。。"""
        p = None
        try_times = 0

        while True:
            try:
                if self.method == 'post':
                    resp = self.pspider.brower.post(url, timeout=self.timeout, params=self.postdata)
                elif self.method == 'get':
                    resp = self.pspider.brower.get(url, timeout=self.timeout, **self.kw)
                else:
                    raise SpiderException(SpiderException.DEFAULT, "不支持其它方法")
                log.info("请求URL={}".format(url))
                log.info("响应字段长度={}".format(len(resp.content)))
                return resp
            except (Timeout, ConnectionError):
                self.pspider.reset_brower()
                try_times += 1
                log.info("重试 ip={} url={} retry={}".format(p, url, try_times))
                if try_times >= self.retry:
                    log.info("超过重试次数 ip={} url={}".format(p, url))
                    break

    def _coro_run(self, urls):
        """
        执行整套流程

        test = TestSpider()
        for i in test.run():
            print(i)         # result
        :param urls:
        :return:
        """

        if isinstance(urls, str):
            urls = deque([urls])
        else:
            urls = deque(urls)

        while True:
            u = urls.popleft()
            resp = self._spider_run(u)
            if resp is None:
                log.info("请求 {} 无数据返回".format(u))
            else:
                parsed = self.handler(resp) # handler函数最后可能返回 list str dict
                # 按照不同的handler进行分类
                # 每个handler只对应一个model实例，一次任务的数据都存在此model实例中
                self.pspider.result[self.result_tag] = parsed
            if len(urls) == 0:
                self.pspider.brower.close() # 释放链接
                break

    def run(self):
        """.返回列表数据"""
        self.parse_func() # 将targets_request中的参数解析出来 url handler

        return self._coro_run(self.urls)


