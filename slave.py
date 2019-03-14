#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-11 11:58
# @Author  : zpy
# @Software: PyCharm

# 用来接收master分发的任务执行
# python3.7 安装supervisor
# pip install git+https://github.com/Supervisor/supervisor.git
#

# todo 完善基本功能
# todo 添加docker
from flask import Flask, request
import xmlrpc.client
import requests

server = xmlrpc.client.ServerProxy('http://127.0.0.1:9001/RPC2')


def register_slave():
    """
    将 slave 注册到系统
    :return:
    """
    requests.get('http://127.0.0.1:5000')

def start_task():
    """
    启动一批任务的进程
    :return:
    """
    pass

def stop_task():
    """
    停止一批任务的进程
    :return:
    """
    pass