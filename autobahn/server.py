#!/usr/bin/env python3

import sys
import inspect
from os import getenv, path

import asyncio
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


current_dir = path.dirname(
    path.abspath(
        inspect.getfile(inspect.currentframe())
    )
)
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from helpers.utils import get_time, byte_to_text  # noqa


HOST = getenv('SOCKET_HOST', '0.0.0.0')
PORT = getenv('SOCKET_PORT', 7642)


def onMessage(data):
    print('.' * 70)
    psize = len(data)
    print('Received data at {}. Packet size in bytes: {} ({})'.format(
        get_time(),
        psize,
        byte_to_text(psize)
    ))
    print(':' * 70)


class ServerProtocol(WebSocketServerProtocol):
    async def onConnect(self, request):
        print('Socket client connected: {}'.format(request.peer))

    async def onOpen(self):
        print('Socket connection opened')

    async def onClose(self, wasClean, code, reason):
        print('Socket connection closed: {}'.format(reason))

    async def onMessage(self, payload, isbinary):
        onMessage(payload)


def startServer():
    factory = WebSocketServerFactory()
    factory.protocol = ServerProtocol
    factory.setProtocolOptions(autoPingInterval=1)
    factory.setProtocolOptions(requireMaskedClientFrames=False)
    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, HOST, PORT)
    server = loop.run_until_complete(coro)
    print('Autobahn server is started at ws://{}:{}'.format(HOST, PORT))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()


if __name__ == '__main__':
    startServer()
