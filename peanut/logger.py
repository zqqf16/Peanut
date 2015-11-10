#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
import logging

from peanut.utils import to_s, to_u

def init_logger(level):
    logging.basicConfig(format='%(message)s', level=level)

_FORMAT = '\033[{}m\033[{};{}m{}\033[0m'

colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
attributes = ['blod', 'underscore', 'blink', 'reverse', 'concealed']

_FOREGROUND = dict(zip(colors, list(range(30, 38))))
_BACKGROUND = dict(zip(colors, list(range(40, 48))))
_attributes = dict(zip(attributes, [1, 4, 5, 7, 8]))

def color(msg, fg, bg=None, attr=None):
    fg_code = _FOREGROUND.get(fg, 39)
    bg_code = _BACKGROUND.get(bg, 49)
    att_code = _attributes.get(attr, 0)
    return _FORMAT.format(att_code, bg_code, fg_code, msg)

def pretty(func, prefix=None, fg=None, bg=None, attr=None):
    def wrapper(msg, *args, **kwargs):
        log = to_s(msg % args)
        if prefx:
            log = prefx + log
        log = color(to_s(log), fg, bg, attr)
        func(log)
    return wrapper

logging.debug = pretty(logging.debug)
logging.info = pretty(logging.info, prefix='👉  ')
logging.warning = pretty(logging.warning, prefix='🌩  ', fg='yellow')
logging.error = pretty(logging.error, prefix='💥  ', fg='red')
logging.critical = pretty(logging.critical, prefix='💀  ', fg='red', attr='blod')


if __name__ == '__main__':
    init_logger(logging.DEBUG)
    logging.debug('hello')
    logging.info('hello')
    logging.warning('hello')
    logging.error('hello')
    logging.critical('hello')
