#!/usr/bin/env python3

import socket
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
from helpers.utils import timing, byte_to_text, \
    get_time, get_memory_usage, generate_bytes_data  # noqa

HOST = getenv('HOST', '0.0.0.0')
PORT = getenv('PORT', 7642)

MAX_PACKET_SIZE = 2 ** 16
SOC_TIMEOUT = 20.0


@timing
def send(message):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(SOC_TIMEOUT)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client.connect((HOST, PORT))

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
        print('Normal memory usage:', byte_to_text(normal_mem_usage, 5))

        client.sendall(message)

        sending_mem_usage = get_memory_usage()
        print(
            'Memory usage while sending:',
            byte_to_text(sending_mem_usage, 5)
        )

    except BaseException as e:
        print(e)
        pass


def init():
    k = 1
    while k <= 24:
        size = 2 ** k
        data = generate_bytes_data(size)
        send(data)
        k += 1


if __name__ == '__main__':
    init()
