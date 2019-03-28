#!/usr/bin/env python3

import time
from datetime import datetime
from os import path, urandom

import psutil


def generate_bytes_data(size):
    return urandom(size)


def ms_to_text(t):
    s = str(round(t / 1000, 2))
    return '{} ({} s)'.format(t, s)


def byte_to_text(bytesize, precision=2):
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'G'),
        (1 << 20, 'M'),
        (1 << 10, 'K'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    if factor == 1:
        precision = 0
    result = bytesize / float(factor)
    if result <= 0:
        return 0
    return '%.*f %s' % (precision, result, suffix)


def get_memory_usage():
    vm = psutil.virtual_memory()
    total = vm.total
    free = vm.available
    used = total - free
    return used


def get_time():
    return datetime.now().strftime('%H:%M:%S')


def timing(f):
    def wrap(*args):
        start = time.time()
        ret = f(*args)
        end = time.time()
        ms = (end - start) * 1000.0
        print('Time to finish sending:', ms_to_text(ms))
        return ret
    return wrap
