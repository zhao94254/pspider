#!/usr/bin/env python
# @Author  : pengyun

from base import get_games, get_room, guess_online
from struct import pack
import re
import json
# import socket
from curio import socket, TaskGroup
import curio
from motor.motor_asyncio import AsyncIOMotorClient
import time
from json import JSONDecodeError
from restart import run_with_restart


def push(data):
    """ 构造发送请求"""
    s = pack('i', 9 + len(data)) * 2
    s += b'\xb1\x02\x00\x00'  # 689
    s += data.encode('ascii') + b'\x00'
    return s

def parse(data):
    """ 解析数据"""
    msg = re.findall(b'(type@=.*?)\x00', data)
    if len(msg) > 0:
        msg = msg[0]
        msg = msg.replace(b'@=', b'":"').replace(b'/', b'","')
        msg = msg.replace(b'@A', b'@').replace(b'@S', b'/')
        try:
            msg = json.loads((b'{"' + msg[:-2] + b'}').decode('utf8', 'ignore'))
        except JSONDecodeError:
            print(msg)
        if not isinstance(msg, bytes) and msg.get('type', '') == 'chatmsg': # 弹幕信息 进入房间信息 礼物信息
            res = {
                'rid': msg.get('rid', '1'),
                'nickname': msg.get('nn', ''),
                'level': msg.get('level', '1'),
                'danmu': msg.get('txt', ''),
                'uid': msg.get('uid', '1')
            }
            return res
    else:
        return ''

def init_db():
    """init db"""
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.crawl
    collection = db.danmu
    return collection

collection = init_db()

class GetDanmu:
    """get danmu use async io"""
    def __init__(self, addr):
        self.max_online, self.max_room = guess_online()
        self.debug = False
        self.keeplive = {}
        self.addr = addr
        self.tmp = []

    def __call__(self, debug=False, *args, **kwargs):
        self.debug = debug
        rooms = self.get_rooms()
        curio.run(self.main(self.addr, rooms))

    async def insert_danmu(self, data):
        if self.debug:
            print('call', data)
            await curio.sleep(0.1)
        else:
            print(data)
            data = [i for i in data if i]
            collection.insert_many(data)
            print("indb", len(data))

    def get_rooms(self):
        """ 获取主播的房间id"""
        games = get_games()
        _room = []
        for i in get_room(games, self.max_online):
            if len(_room) > self.max_room:
                break
            _room.extend(i)
        return _room

    async def preconn(self, addr, room_id):
        """ 一个链接对应一个房间  """
        connect = await socket.create_connection(addr)
        pushdata = push('type@=loginreq/roomid@={}/'.format(room_id))
        await connect.sendall(pushdata)
        pre_recv = await connect.recv(9999)
        return connect

    async def get_danmu(self, addr, room_id):
        connect = await self.preconn(addr, room_id)
        data = push('type@=joingroup/rid@={}/gid@=-9999/'.format(room_id))
        await connect.sendall(data)
        if room_id not in self.keeplive:
            self.keeplive[room_id] = time.time()
        while True:
            recv_danmu = await connect.recv(9999)
            if not recv_danmu:
                break
            # 保持链接。
            # keeplive = 3
            if time.time() - self.keeplive[room_id] > 25:
                data = push('type@=keeplive/tick@=%s/' % int(time.time()))
                self.keeplive[room_id] = time.time()
                await connect.sendall(data)
            # save -->
            self.tmp.append(parse(recv_danmu))
            if len(self.tmp) >= 800:
                indb = self.tmp[:]
                self.tmp = []
                await self.insert_danmu(indb)

    async def main(self, addr, rooms):
        async with TaskGroup() as g:
            for i in rooms:
                await g.spawn(self.get_danmu(addr, i))

def start():
    addr = ('openbarrage.douyutv.com', 8601)
    getdanmu = GetDanmu(addr)
    getdanmu()

if __name__ == '__main__':
    run_with_restart(start, stime=time.time(), retime=1200, )









