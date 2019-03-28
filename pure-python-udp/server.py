#!/usr/bin/env python3

import socketserver
import sys
import inspect
from os import getenv, path

current_dir = path.dirname(
    path.abspath(
        inspect.getfile(inspect.currentframe())
    )
)
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from helpers.utils import get_time, byte_to_text  # noqa

HOST = getenv('HOST', '0.0.0.0')
PORT = getenv('PORT', 7642)

MAX_PACKET_SIZE = 2 ** 16


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print('.' * 70)
        psize = len(data)
        print('Received data at {}. Packet size in bytes: {} ({})'.format(
            get_time(),
            psize,
            byte_to_text(psize)
        ))
        print(':' * 70)


def startServer():
    server = socketserver.UDPServer((HOST, PORT), UDPHandler)
    server.max_packet_size = MAX_PACKET_SIZE
    print('WebSocket UDP server is started at ws://{}:{}'.format(HOST, PORT))
    server.serve_forever()
    return server


if __name__ == '__main__':
    startServer()
