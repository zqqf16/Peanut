#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Peanut

Usage:
  peanut init [-v] [<directory>]
  peanut [-v] [-c | --config <config_file_path>] [<directory>]
  peanut (-h | --help)
  peanut --version

Options:
  -c --config   Config file path.
  -v            Visiable.
  -h --help     Show help.
  --version     Show version.
"""

import logging
from docopt import docopt

import peanut
from peanut import site


def main():
    """Read command line arguments and generate site
    """
    args = docopt(__doc__, version='Peanut '+peanut.version)

    directory = args.get('<directory>', './') or './'
    config_path = args.get('<config_file_path>', None)

    if args['init']:
        logging.info('Init ...')
        site.Site.init()
        logging.info('Done')
        exit(0)

    logging.info('Generating ...')
    blog = site.Site(directory, config_path)
    blog.generate()
    logging.info('Done')

if __name__ == '__main__':
    main()
