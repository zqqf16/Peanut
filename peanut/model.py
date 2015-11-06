#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Post, Tag and Category
"""

from __future__ import unicode_literals

from datetime import datetime

from peanut.utils import path_to_url, url_safe
from peanut.options import configs, env


class Post(object):
    """Post model
    """

    layout = 'post'

    def __init__(self, title, slug, content=None, meta=None):
        self.title = title
        self.slug = slug
        self.content = content

        meta = meta or {}
        self.date = meta.pop('date', None) or datetime.now()
        self.publish = meta.pop('publish', True)
        self.layout = meta.pop('layout', Post.layout)
        self.top = meta.pop('top', False)
        self.tags = meta.pop('tags', [])

        self.meta = meta

    def __getattr__(self, key):
        try:
            return super(Post, self).__getattr__(key)
        except:
            pass
        return self.meta.get(key)

    @property
    def url(self):
        relative_url = path_to_url(self.file_path)
        if not relative_url.startswith('/'):
            relative_url = '/'+relative_url
        return relative_url

    @property
    def file_path(self):
        template = configs.path.post
        return url_safe(template.format(**self.__dict__))
