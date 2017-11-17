#!/usr/bin/env python
# @Author  : pengyun

# 获取基本的信息
import requests
import redis
import curio
from datetime import datetime

r = redis.StrictRedis(host='localhost', port=6379, db=0)

rooms = {'max': [],'min': []}
useronline = {}
fans = {}

def guess_online():
    hour = int(str(datetime.now())[11:13])
    if 0 < hour <= 10:
        return 5000, 200
    elif 10 < hour <= 16:
        return 15000, 150
    else:
        return 40000, 90

def get_games():
    """ 获取频道的信息"""
    games = requests.get('http://open.douyucdn.cn/api/RoomApi/game').json()['data']  # 获取所有的频道

    games_info = {
        i['short_name']: {'game_icon': i['game_icon'], 'game_name': i['game_name'], 'short_name': i['short_name']} for i in games
    }  # 转化为需要的格式
    return games_info


def get_room(games, max_online):
    room_info = {}
    for i in games:
        gamelink = 'http://api.douyu.com/api/v1/live/{}'.format(i)
        game_data = requests.get(gamelink) # 频道在线主播信息
        if game_data.status_code == 200 and game_data.json()['error'] == 0:
            game_data = game_data.json()['data']
        else:
            continue

        game_online = sum([i['online'] for i in game_data]) # 频道总在线人数
        games[i]['online'] = game_online
        # 这个数据直接放在redis里

        rooms_id = []
        for j in game_data:
            if j['online'] > max_online:
                rooms_id.append(j['room_id'])
                room_info[j['room_id']] = {
                    'online': j['online'],
                    'nickname': j['nickname'],
                    'fans': j['fans'],
                    'image_link': j['avatar_mid'],
                    'games': i,
                }
        o_num = [g['online'] for g in game_data if g['online']>max_online]
        if len(o_num) > 0:
        #     print("online numbers", sum(o_num), "rooms", len(o_num))
            r.set('online|{}'.format(i), (sum(o_num), len(o_num)))
        yield rooms_id
    # return games, room_info

if __name__ == '__main__':
    max_online, _ = guess_online()

    games = get_games()
    for i in get_room(games, max_online):
        print(i)