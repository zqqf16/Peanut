#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging

from peanut import site


def cli():
    """Command line interface
    """
    parser = argparse.ArgumentParser(description='Static blog generator')

    parser.add_argument('dir', nargs='?', help='Blog directory')
    parser.add_argument('-c', '--config', help='Config file path')

    args = parser.parse_args()

    return {
        'directory': args.dir or '.',
        'config_path': args.config or None
    }

def main():
    """Read command line arguments and generate site
    """
    args = cli()
    blog = site.Site(args['directory'], args['config_path'])
    blog.generate()

if __name__ == '__main__':
    main()
