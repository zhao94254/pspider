#!/usr/bin/env python
# @Author  : pengyun

import asyncio
import cgi
import re
from datetime import datetime
from asyncio import Queue
import aiohttp
from lxml import etree
from collections import OrderedDict
import time
import motor.motor_asyncio
import argparse
from concurrent import futures


def is_root_url(url):
    """判断是否是根"""
    if len(url) < 40:
        return True
    return False


def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient('mondodb server')
    db = client.document
    collection = db.collection
    return collection

# setting.
collection = init_db()
sleep_interval = 0.1

async def insert(data):
    indb = await collection.find_one({'href': data['href']})
    if indb:
        await asyncio.sleep(0.001)
    else:
        await collection.insert(data)


def get_page_url(baseurl, endpoint, start, end):
    # 根据baseurl获取要获取的url

    start = 1 if start == 0 else start
    page = start
    while page < end:
        yield baseurl + endpoint + str(page) + '/'
        page += 1


class Crawler:
    def __init__(self, roots, baseurl,
                 max_tries=4, max_tasks=10, _loop=None):
        self.loop = _loop or asyncio.get_event_loop()
        self.roots = roots
        self.baseurl = baseurl
        self.prefix_url = self.baseurl[:-1]
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.urls_queue = Queue(loop=self.loop)
        self.seen_urls = set()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.href_house = {}
        for root in roots:
            self.urls_queue.put_nowait(root)

        self.started_at = datetime.now()
        self.end_at = None

    def close(self):
        self.session.close()

    @staticmethod
    async def fetch_etree(response):
        """将响应转化为etree格式的"""
        if response.status == 200:
            content_type = response.headers.get('content-type')
            if content_type:
                content_type, _ = cgi.parse_header(content_type)
            if content_type in ('text/html', 'application/xml'):
                text = await response.text()
                doc = etree.HTML(text)
                return doc

    def _parse_root_per_house(self, house_box, count):
        """解析第一级页面"""
        house_dict = OrderedDict()
        child = '//li[{}]'.format(count)
        try:
            href = house_box.xpath(
                child + '/div[2]/h2/a/@href')[0]
            house_dict['href'] = href
            self.seen_urls.add(href)

            house_dict['title'] = house_box.xpath(
                child + '/div[2]/h2/a/text()')[0]

            house_dict['compound'] = house_box.xpath(
                child + '/div[2]/div[1]/div[1]/a/span/text()')[0].strip()

            house_dict['layout'] = house_box.xpath(
                child + '/div[2]/div[1]/div[1]/span[1]/span[1]/text()')[0].strip()

            house_dict['gross_floor_area'] = house_box.xpath(child + '/div[2]/div[1]/div[1]/span[2]/text()')[0].strip()

            house_dict['distribute'] = house_box.xpath(
                child + '/div[2]/div[1]/div[2]/div/a[1]/text()')[0]

            house_dict['floor'] = ''.join(house_box.xpath(
                child + '/div[2]/div[1]/div[2]/div/text()'))

            house_dict['orientation'] = house_box.xpath(
                child + '/div[2]/div[1]/div[1]/span[3]/text()')

            house_dict['rent_per_month'] = house_box.xpath(
                child + '/div[2]/div[2]/div[1]/span/text()')[0]

            house_dict['added_at'] = house_box.xpath(
                child + '/div[2]/div[2]/div[2]/text()')[0][:10]

            house_dict['total_views'] = house_box.xpath(
                child + '/div[2]/div[3]/div/div[1]/span/text()')[0]
        except IndexError as e:
            print('catch error')

        try:
            subway_detail = house_box.xpath(
                child + '/div[2]/div[1]/div[3]/div/div/span[2]/span/text()')[0]
            _matched = re.search('距离(.*?)号线(.*?)[站+](.*?)米', subway_detail, re.S)
            if _matched:
                house_dict['subway_line'] = _matched.group(1)
                house_dict['subway_station'] = _matched.group(2)
                house_dict['subway_distance'] = _matched.group(3)
        except IndexError:
            house_dict['subway_line'] = None
            house_dict['subway_station'] = None
            house_dict['subway_distance'] = None
        return house_dict

    async def parse_root_etree(self, doc):
        houses_select = '//*[@id="house-lst"]/li'
        houses_list = doc.xpath(houses_select)
        count = 0
        for house_box in houses_list:
            count += 1
            house_dict = self._parse_root_per_house(house_box, count)
            second_level_url = house_dict['href']
            self.href_house[second_level_url] = house_dict
            self.urls_queue.put_nowait(second_level_url)
        await asyncio.sleep(sleep_interval)

    async def parse_second_etree(self, doc, href):
        assert href in self.href_house.keys()
        assert href in self.seen_urls

        house_dict = self.href_house[href]
        house_dict['number'] = href[len(self.baseurl + 'zufang/'):-5]

        if doc is not None:
            location = doc.xpath('/html/body/div[4]/script[10]/text()')[0].strip()
            location = location[location.find('Position') + 10:location.find('cityId') - 9].split(',')
            house_dict['location'] = location

            try:
                house_dict['latest_week_views'] = doc.xpath(
                    '//*[@id="record"]/div[2]/div[2]/text()')[0]
            except IndexError:
                house_dict['latest_week_views'] = None
        else:
            house_dict['address'] = None
            house_dict['latest_week_views'] = None

        if doc is None:
            house_dict['img_url'] = None
        else:
            img_tmp = []

            for count, img_box in enumerate(doc.xpath('//*[@id="topImg"]/div[2]/ul/li'), start=1):
                img_src = img_box.xpath('//img/@src'.format(count))[0]
                img_tmp.append(img_src)
            house_dict['img_url'] = img_tmp

        house_dict['captured_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 插入数据
        await insert(house_dict)
        del self.href_house[href]

    async def handle(self, url):
        tries = 0
        # 尝试max_tries次
        while tries < self.max_tries:
            try:
                response = await self.session.get(
                    url, allow_redirects=False)
                break
            except aiohttp.ClientError:
                pass
            tries += 1
        try:
            doc = await self.fetch_etree(response)
            if is_root_url(url):
                print('root:{}'.format(url))
                await self.parse_root_etree(doc)
            else:
                print('second level:{}'.format(url))
                await self.parse_second_etree(doc, url)
        finally:
            await response.release()

    async def work(self):
        try:
            while True:
                url = await self.urls_queue.get()
                await self.handle(url)
                # 防止流量异常
                time.sleep(sleep_interval)
                self.urls_queue.task_done()
        except asyncio.CancelledError:
            pass

    async def run(self):
        workers = [asyncio.Task(self.work(), loop=self.loop)
                   for _ in range(self.max_tasks)]
        self.started_at = datetime.now()
        await self.urls_queue.join()
        self.end_at = datetime.now()
        for w in workers:
            w.cancel()


def start(args):
    start, end = args
    endpoint = 'zufang/pg'
    loop = asyncio.get_event_loop()
    baseurl = 'https://bj.lianjia.com/'
    crawler = Crawler(get_page_url(baseurl, endpoint, start, end), max_tasks=30, baseurl=baseurl)
    loop.run_until_complete(crawler.run())

    print('Finished {0} urls in {1} secs'.format(
        len(crawler.seen_urls),
        (crawler.end_at - crawler.started_at).total_seconds()))

    crawler.close()
    loop.close()


def mul_start(task):
    """将任务分配到多核 并行处理"""
    import os
    cpus = os.cpu_count()
    t = task // cpus
    tasks = [(i*t, (i+1)*t) for i in range(cpus)]
    with futures.ProcessPoolExecutor() as executor:
        executor.map(start, tasks)


def main():
    parser = argparse.ArgumentParser(description="Run crawl")
    parser.add_argument('-m', dest='method', help="m--mulprocess n--normal")
    parser.add_argument('-t', dest='task', help="you want crawl page number")
    args = parser.parse_args()
    if args.method == 'm':
        mul_start(int(args.task))
    elif args.method == 'n':
        start((1, int(args.task)))
    else:
        print("Please check your input")


if __name__ == '__main__':
    main()

