#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import builtins

try:
    from urllib.parse import urljoin, urlsplit
    from urllib.request import pathname2url, url2pathname
except:
    from urlparse import urljoin, urlsplit
    from urllib import pathname2url, url2pathname

def to_s(value):
    return str(value)

def to_u(value):
    return str(value)

def path_to_url(path):
    return pathname2url(path)

def url_to_path(url):
    return url2pathname(url)

def url_safe(string):
    new_str = re.sub(
            r'[<>,~!#&\{\}\(\)\[\]\*\^\$\?]', ' ', string
    )

    return '-'.join(new_str.strip().split())

def real_url(base, url):
    path = urlsplit(base).path
    if not path.endswith('/'):
        path = path + '/'
    url = url.lstrip('/')
    return urljoin(path, url)

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


def list_dir(path):
    """List all unhidden files
    """
    for filename in os.listdir(path):
        if filename.startswith('.'):
            continue
        if os.path.isdir(filename):
            continue
        yield to_u(os.path.join(path, filename))

def get_resource(relative_path):
    package_path = os.path.abspath(os.path.split(__file__)[0])
    return os.path.join(package_path, relative_path)
