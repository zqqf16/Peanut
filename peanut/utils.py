#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin


def package_resource(path):
    """Get resource from package

    @param path: the relative path of resource

    @return: the absolute path of resource
    """

    curr_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.abspath(os.path.join(curr_path, path))


def walk_directory(path, abs_path=True):
    """Generate directory tree

    @param path: the directory to be walked
    @param abs_path: return absolute file path or not

    @return: dictionary, doesn't include the files start with '.'
    """

    tree = {'dirs':{}, 'files':[]}

    for f in os.listdir(path):
        if f.startswith('.'):
            continue

        p = os.path.join(path, f)
        if os.path.isdir(p):
            d = walk_directory(os.path.join(p))
            tree['dirs'][p] = d

        if os.path.isfile(p):
            tree['files'].append(p)

    return tree
