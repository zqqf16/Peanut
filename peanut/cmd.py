#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Peanut

Usage:
  peanut init [(-v|-d)] [<directory>]
  peanut [(-v|-d)] [-c | --config <config_file_path>] [<directory>]
  peanut (-h | --help)
  peanut --version

Options:
  -c --config   Config file path.
  -v            Visiable.
  -d            Show Debug.
  -h --help     Show help.
  --version     Show version.
"""

import logging
from docopt import docopt

import peanut
from peanut import site
from peanut.logger import init_logger

def main():
    """Read command line arguments and generate site
    """
    args = docopt(__doc__, version='Peanut '+peanut.version)

    directory = args.get('<directory>', './') or './'
    config_path = args.get('<config_file_path>', None)

    visiable = args.get('-v', False)
    debug = args.get('-d', False)

    if debug:
        init_logger(logging.DEBUG)
    elif visiable:
        init_logger(logging.VISIABLE)
    else:
        init_logger(logging.INFO)

    if args['init']:
        logging.info('Init peanut environments')
        site.Site.init(directory)
        exit(0)

    blog = site.Site(directory)

    logging.info('Loading configurations...')
    try:
        blog.load_config(config_path)
    except Exception as e:
        logging.critical(e.args[0])
        exit(-1)

    logging.info('Generating...')
    blog.generate()

if __name__ == '__main__':
    main()
