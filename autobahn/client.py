#!/usr/bin/env python3

import socket
import sys
import inspect
from os import getenv, path

import asyncio

from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


current_dir = path.dirname(
    path.abspath(
        inspect.getfile(inspect.currentframe())
    )
)
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from helpers.utils import timing, byte_to_text, \
    get_time, get_memory_usage, generate_bytes_data  # noqa


HOST = getenv('HOST', '0.0.0.0')
PORT = getenv('PORT', 7642)


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print('Server connected: {}'.format(response.peer))

    def onOpen(self):
        print('WebSocket connection opens')

        @timing
        def send(message):
            try:
                print('.' * 70)
                print('Sending data at {}'.format(get_time()))
                normal_mem_usage = get_memory_usage()
                msg_size = len(message)
                print(
                    'Packet size in bytes: {} ({})'.format(
                        msg_size,
                        byte_to_text(msg_size)
                    )
                )
                print(
                    'Normal memory usage:',
                    byte_to_text(normal_mem_usage, 5)
                )

                self.sendMessage(message, isBinary=True)

                sending_mem_usage = get_memory_usage()
                print(
                    'Memory usage while sending:',
                    byte_to_text(sending_mem_usage, 5)
                )
            except Exception as err:
                print(err)
                pass

        k = 1
        while k <= 24:
            size = 2 ** k
            data = generate_bytes_data(size)
            send(data)
            k += 1

    def onMessage(self, payload, isBinary):
        print('Received: {} bytes'.format(len(payload)))

    def onClose(self, wasClean, code, reason):
        print('WebSocket connection closed: {}'.format(reason))


def init():
    try:
        factory = WebSocketClientFactory('ws://{}:{}'.format(HOST, PORT))
        factory.protocol = MyClientProtocol
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(factory, HOST, PORT)
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()
    except Exception as err:
        print('Error while trying to start socket client:')
        print(err)


if __name__ == '__main__':
    init()
