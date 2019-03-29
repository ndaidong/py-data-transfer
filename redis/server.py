#!/usr/bin/env python3

import time
import sys
import inspect
from os import getenv, path

import redis


current_dir = path.dirname(
    path.abspath(
        inspect.getfile(inspect.currentframe())
    )
)
parent_dir = path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from helpers.utils import get_time, byte_to_text  # noqa


HOST = getenv('REDIS_HOST', '0.0.0.0')
PORT = getenv('REDIS_PORT', 7642)
CHANNEL = 'chan'


def onMessage(data):
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
        print('Redis server is started at ws://{}:{}'.format(HOST, PORT))
        r = redis.Redis(host=HOST, port=PORT, db=0)
        p = r.pubsub()
        p.subscribe(CHANNEL)
        while True:
            message = p.get_message()
            if message and message['type'] == 'message' \
                    and message['data']:
                onMessage(message['data'])
            time.sleep(0.001)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    startServer()
