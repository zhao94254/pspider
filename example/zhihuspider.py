# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 19:19
# @Author  : py
# @Email   : zpy94254@gmail.com
# @File    : zhihuspider.py
# @Software: PyCharm

from spider.pspider import Pspider, req
from spider.model import BaseModel

class BihuSpider(Pspider):

    def task(self):
        # p =  'pyy-69-54'
        # return 'https://www.zhihu.com/api/v4/members/{}/followees?offset=0&limit=20'.format(p)
        return self.tasks

    def req_resp(self):
        @req()
        def pages():
            url = self.task()
            return {"request": {
                'url': url,
            },
                "response": {
                    "handler": self.parse_data,
                    "result_tag": 'data'
                }}
        yield pages

    def parse_data(self, resp):
        if resp.json()['paging']['is_end']:
            npage = ''
        else:
            npage = resp.json()['paging']['next'].replace('members', 'api/v4/members')
        res = {
            'next_page': npage,
            'data': list(map(lambda x:{'name':x['name'], 'url_token':x['url_token']}, resp.json()['data']))
        }

        return res

if __name__ == '__main__':
    sp = BihuSpider()
    sp.tasks = 'https://www.zhihu.com/api/v4/members/pyy-69-54/followees?limit=20&offset=40'
    sp.start()
    print(sp.result['data'])