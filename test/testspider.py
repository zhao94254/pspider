#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-14 10:33
# @Author  : zpy
# @Software: PyCharm

from spider.pspider import Pspider, req
from spider.model import BaseModel

class LagouSpider(Pspider):

    def task(self):
        return self.tasks

    def req_resp(self):
        self.jobmodel = BaseModel(
            [('company', str), ('companyid', str), ('positionname', str), ('salary', str), ('require', str)])
        @req()
        def pages():
            url = self.task()
            return {"request": {
                'url': url,
            },
                "response": {
                    "handler": self.parse_data,
                    "result_tag": 'job'
                }}
        yield pages

    def parse_data(self, resp):

        for d in resp.html.xpath('//*[@id="s_position_list"]/ul/li'):
            self.jobmodel.res.require = ''.join(d.xpath('//div[1]/div[1]/div[2]/div/text()'))
            self.jobmodel.res.company = d.attrs.get('data-company')
            self.jobmodel.res.companyid = d.attrs.get('data-companyid')
            self.jobmodel.res.salary = d.attrs.get('data-salary')
            self.jobmodel.res.positionname = d.attrs.get('data-positionname')
            self.jobmodel.save()
        return self.jobmodel

if __name__ == '__main__':
    sp = LagouSpider()
    sp.tasks = ['https://www.lagou.com/zhaopin/Python/1']
    sp.start()

    for s in sp.result['job'].export_sql('test.test'):
        print(s)