#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/2/2 下午5:12
# @Author  : zpy
# @Software: PyCharm


from socket import *
import argparse

# nc localhost port .
def start_tcp_server(port):
    """ 测试go tcp.  """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    sock.bind(('localhost', port))
    sock.listen(5)
    with sock:
        client, addr = sock.accept()
        while True:
            recv = client.recv(1024)
            client.sendall(recv)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run a tcp server")
    parser.add_argument("-p", "-port", dest="port", default=False)
    args = parser.parse_args()

    start_tcp_server(int(args.port))
