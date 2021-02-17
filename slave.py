#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2019-03-11 11:58
# @Author  : zpy
# @Software: PyCharm

# 用来接收main分发的任务执行
# python3.7 安装supervisor
# pip install git+https://github.com/Supervisor/supervisor.git

base_supconf = """
; subordinate config

[unix_http_server]
file=/Users/mioji/suptest/supervisor.sock   ; the path to the socket file

[inet_http_server]         ; inet (TCP) server disabled by default
port=127.0.0.1:9001        ; ip_address:port specifier, *:port for all iface

[supervisord]
logfile=/Users/mioji/suptest/log/supervisord.log ; main log file; default $CWD/supervisord.log
logfile_maxbytes=50MB        ; max main logfile bytes b4 rotation; default 50MB
logfile_backups=10           ; # of main logfile backups; 0 means none, default 10
loglevel=info                ; log level; default info; others: debug,warn,trace
pidfile=/Users/mioji/suptest/supervisord.pid ; supervisord pidfile; default supervisord.pid
nodaemon=false               ; start in foreground if true; default false
minfds=1024                  ; min. avail startup file descriptors; default 1024
minprocs=200                 ; min. avail process descriptors;default 200

; rpc ..
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///Users/mioji/suptest/supervisor.sock ; use a unix:// URL  for a unix socket
serverurl=http://127.0.0.1:9001 ; use an http:// url to specify an inet socket
; subordinate
[program:subordinate]
directory=/Users/mioji/Desktop/newpy/github/pspider
command=/Users/mioji/skrskr/bin/python  subordinate.py
stdout_logfile=/Users/mioji/suptest/%(program_name)s_out.log
stdout_logfile_maxbytes=512MB
stdout_logfile_backups=4
stderr_logfile=/Users/mioji/suptest/%(program_name)s_err.log
stderr_logfile_maxbytes=512MB
stderr_logfile_backups=4
stderr_capture_maxbytes=512MB
"""

fmt = """
[program:{program}]
directory={directory}
command={command}
numprocs=1
autostart=true
startsecs=1
startretries=3
autorestart=true
stopsignal=QUIT
stopwaitsecs=10
stdout_logfile=/Users/mioji/suptest/log/%(program_name)s_out.log
stdout_logfile_maxbytes=512MB
stdout_logfile_backups=4
stderr_logfile=/Users/mioji/suptest/log/%(program_name)s_err.log
stderr_logfile_maxbytes=512MB
stderr_logfile_backups=4
stderr_capture_maxbytes=512MB
"""

# todo 完善基本功能
# todo 添加docker
from flask import Flask, request
import xmlrpc.client
import requests
import json

app = Flask(__name__)
server = xmlrpc.client.ServerProxy('http://127.0.0.1:9001/RPC2')

def build_conf(proglst):
    """
    构建配置文件
    :return:
    """
    yield base_supconf
    for p in proglst:
        yield fmt.format(**p)

def update_conf(proglst):
    with open("/Users/mioji/suptest/supconf.conf", 'w') as f:
        for conf in build_conf(proglst):
            f.write(conf)

def register_subordinate():
    """
    将 subordinate 注册到系统
    :return:
    """
    requests.get('http://127.0.0.1:5000')

@app.route('/', methods=['GET', 'POST'])
def start_task():
    """
    启动一批任务的进程
    main 请求此接口，subordinate将配置文件构建好，调用supervisor的rpc 将进程启动
    :return:
    """
    proglst = json.loads(request.form['proglst'])

    update_conf(proglst)
    server.supervisor.reloadConfig()
    server.supervisor.restart()
    return 'update success'

def stop_task():
    """
    停止一批任务的进程
    :return:
    """
    pass

if __name__ == '__main__':
    # test subordinate
    # requests.post('http://127.0.0.1:5001/', data={'proglst': '[{"directory": "/Users/mioji/Desktop/newpy/github/pspider", "command": "/Users/mioji/skrskr/bin/celery -A app worker", "program": "test"}]'
    # })
    register_subordinate()
    app.run(port=5001, debug=True)