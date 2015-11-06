#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import six

try:
    from urllib.parse import urljoin
    from urllib.request import pathname2url, url2pathname
except:
    from urlparse import urljoin
    from urllib import pathname2url, url2pathname

def path_to_url(path):
    if six.PY2:
        path = path.encode('utf-8')
    return pathname2url(path)

def url_to_path(url):
    if six.PY2:
        url = url.encode('utf-8')
    return url2pathname(url)

def url_safe(string):
    new_str = re.sub(
            r'[<>,~!#&\{\}\(\)\[\]\*\^\$\?]', ' ', string
    )

    return '-'.join(new_str.strip().split())


def package_resource(path):
    """Get resource from package

    @param path: the relative path of resource

    @return: the absolute path of resource
    """

    curr_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.abspath(os.path.join(curr_path, path))


def neighborhood(alist):
    """Get neighborhood when looping"""

    length = len(alist)
    if length == 0:
        return

    prev = None
    curr = None
    next = None

    for i, curr in enumerate(alist):
        if i > 0:
            prev = alist[i-1]
        if i+1 < length:
            next = alist[i+1]
        yield (prev, curr, next)
    yield (prev, curr, None)


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
