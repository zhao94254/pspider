#!/usr/bin/env python
# @Author  : pengyun

from base import get_games, get_room
from struct import pack
import re
import json
# import socket
from curio import socket, TaskGroup
import curio

max_online = 50000
max_room = 20

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
        msg = json.loads((b'{"' + msg[:-2] + b'}').decode('utf8', 'ignore'))
        if msg.get('type', '') == 'chatmsg': # 弹幕信息 进入房间信息 礼物信息
            # print(msg)
        # return msg.get('nn', ''), msg.get('rid', '')
            return msg
    return ''

async def get_danmu(addr, room_id):
    connect = await preconn(addr, room_id)
    data = push('type@=joingroup/rid@={}/gid@=-9999/'.format(room_id))
    await connect.sendall(data)
    while True:
        recv_danmu = await connect.recv(9999)
        if not recv_danmu:
            break
        # save -->
        print(parse(recv_danmu))

async def main(addr, room_ids):
    async with TaskGroup() as g:
        for i in room_ids:
            await g.spawn(get_danmu(addr, i))

if __name__ == '__main__':
    rooms = get_rooms()
    addr = ('openbarrage.douyutv.com', 8601)
    curio.run(main(addr, rooms))


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








