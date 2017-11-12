#!/usr/bin/env python
# @Author  : pengyun

from base import get_games, get_room
from struct import pack
import re
import json
import socket

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


def start():
    addr = ('openbarrage.douyutv.com', 8601)
    roomid = get_rooms()[0]
    print(roomid)
    connect = socket.create_connection(addr)

    pushdata = push('type@=loginreq/roomid@={}/'.format(roomid))
    data = push('type@=joingroup/rid@={}/gid@=-9999/'.format(roomid))

    connect.sendall(pushdata)
    recv1 = connect.recv(9999)
    # print(recv1)

    connect.sendall(data)
    while True:
        recv2 = connect.recv(9999)
        if not recv2:
            break
        print(parse(recv2))

if __name__ == '__main__':
    start()







