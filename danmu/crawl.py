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

max_online, max_room = guess_online()
debug = False
times = 0
keeplive = time.time()
tmp = []

def init_db():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.crawl
    danmu = db.danmu
    return danmu

collection = init_db()

async def insert_danmu(data):
    if debug:
        print('call', data)
        await curio.sleep(0.1)
    else:
        data = [i for i in data if i]
        collection.insert_many(data)


def get_rooms():
    """ 获取主播的房间id"""
    games = get_games()
    _room = []
    for i in get_room(games, max_online):
        if len(_room) > max_room:
            break
        _room.extend(i)
    return _room

def push(data):
    """ 构造发送请求"""
    s = pack('i', 9 + len(data)) * 2
    s += b'\xb1\x02\x00\x00'  # 689
    s += data.encode('ascii') + b'\x00'
    return s

async def preconn(addr, room_id):
    """ 应该是 建立一个链接 --》 preconn 多个房间 —》获取弹幕 """
    connect = await socket.create_connection(addr)
    pushdata = push('type@=loginreq/roomid@={}/'.format(room_id))
    await connect.sendall(pushdata)
    pre_recv = await connect.recv(9999)
    return connect

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
            # print(msg)
            # return msg.get('nn', ''), msg.get('rid', '')
            res = {
                'rid': msg.get('rid', '1'),
                'nickname': msg.get('nn', ''),
                'level': msg.get('level', '1'),
                'danmu': msg.get('txt', ''),
                'uid': msg.get('uid', '1')
            }
            return res
    return ''

async def get_danmu(addr, room_id):
    connect = await preconn(addr, room_id)
    data = push('type@=joingroup/rid@={}/gid@=-9999/'.format(room_id))
    await connect.sendall(data)
    while True:
        recv_danmu = await connect.recv(9999)
        if not recv_danmu:
            break
        # 保持链接。
        global times, keeplive, tmp
        if time.time() - keeplive > 25:
            data = push('type@=keeplive/tick@=%s/' % int(time.time()))
            keeplive = time.time()
            await connect.sendall(data)
        # save -->
        tmp.append(parse(recv_danmu))
        if len(tmp) >= 800:
            indb = tmp[:]
            tmp = []
            await insert_danmu(indb)

async def main(addr, room_ids):
    async with TaskGroup() as g:
        for i in room_ids:
            await g.spawn(get_danmu(addr, i))

def start():
    rooms = get_rooms()
    addr = ('openbarrage.douyutv.com', 8601)
    curio.run(main(addr, rooms))

if __name__ == '__main__':
    run_with_restart(start, stime=time.time(), retime=1200, )


# def start():
#     addr = ('openbarrage.douyutv.com', 8601)
#     roomid = get_rooms()[0]
#     print(roomid)
#     connect = socket.create_connection(addr)
#
#     pushdata = push('type@=loginreq/roomid@={}/'.format(roomid))
#     data = push('type@=joingroup/rid@={}/gid@=-9999/'.format(roomid))
#
#     connect.sendall(pushdata)
#     recv1 = connect.recv(9999)
#     print(recv1)
#
#     connect.sendall(data)
#     while True:
#         recv2 = connect.recv(9999)
#         if not recv2:
#             break
#         print(parse(recv2))








