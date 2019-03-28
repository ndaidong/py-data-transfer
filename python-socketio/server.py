#!/usr/bin/env python3

import sys
import inspect
from os import getenv, path

import eventlet
import socketio


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
NAMESPACE = '/ns'


sio = socketio.Server(async_mode='eventlet')
app = socketio.Middleware(sio)


@sio.on('connect', namespace=NAMESPACE)
def connect(sid, environ):
    print('Connection established with', sid)


@sio.on('message', namespace=NAMESPACE)
def message(sid, data):
    print('.' * 70)
    psize = len(data)
    print('Received data at {}. Packet size in bytes: {} ({})'.format(
        get_time(),
        psize,
        byte_to_text(psize)
    ))
    print(':' * 70)


def startServer():
    try:
        print('SocketIO server is started at ws://{}:{}'.format(HOST, PORT))
        eventlet.wsgi.server(
            eventlet.listen((HOST, PORT)),
            app,
            log_output=False
        )
    except Exception as err:
        print(err)


if __name__ == '__main__':
    startServer()
