#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Post, Tag and Category
"""

from __future__ import unicode_literals

import re
import os
from datetime import datetime

from peanut.utils import path_to_url, url_safe, real_url
from peanut.options import configs, env


class BaseModel(object):
    """Base model class
    """

    layout = None

    @property
    def file_path(self):
        template = configs.path.get(self.__class__.layout, '').lstrip('/')
        return url_safe(template.format(**self.__dict__))

    @property
    def url(self):
        relative_url = path_to_url(self.file_path)
        if not relative_url.startswith('/'):
            relative_url = '/'+relative_url
        return real_url(configs.site.url, relative_url)


class Tag(BaseModel):
    """Tag model
    """

    layout = 'tag'

    def __init__(self, title):
        self.title = title
        self.slug = url_safe(title)

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)


class Post(BaseModel):
    """Post model
    """

    layout = 'post'

    def __init__(self, title, slug, content=None, meta=None):
        self.title = title
        self.slug = url_safe(slug)
        self.content = content

        meta = meta or {}
        self.date = meta.pop('date', None) or datetime.now()
        self.publish = meta.pop('publish', True)
        self.layout = meta.pop('layout', Post.layout)
        self.top = meta.pop('top', False)
        self.tag_titles = meta.pop('tags', [])

        self.meta = meta

    @property
    def tags(self):
        return [Tag(t) for t in self.tag_titles]

    def __getattr__(self, key):
        try:
            return super(Post, self).__getattr__(key)
        except:
            pass
        return self.meta.get(key)

    def __lt__(self, other):
        return self.date < other.date


class Pagination(object):
    """Pagination"""

    def __init__(self, posts, page=1, base_url=None, posts_per_page = 5):
        self._posts = posts
        # page number starts from 1
        self.page = page
        self.base_url = base_url
        if posts_per_page == 0:
            posts_per_page = len(self._posts)
        self.posts_per_page = posts_per_page

        self.path = None
        self.url = None
        self.parse_path_and_url()

    def parse_path_and_url(self):
        template = configs.path.pagination
        relative_path = template.format(
            number=self.page,
            num=self.page,
            n=self.page
        )

        if self.page == 1:
            relative_path = ''

        file_path = None
        url = None
        if re.search(r'index.html?$', self.base_url):
            # If base_url ends with index.html or index.htm,
            # insert page path before the index.*
            parent, index = os.path.split(self.base_url)
            url = file_path = os.path.join(parent, relative_path, index)
        else:
            if not self.base_url.endswith('/'):
                self.base_url = self.base_url + '/'
            else:
                if relative_path != '' and not relative_path.endswith('/'):
                    relative_path = relative_path + '/'
            url = os.path.join(self.base_url, relative_path)
            file_path = os.path.join(url, 'index.html')

        if not url.startswith('/'):
            url = '/' + url
        if file_path.startswith('/'):
            file_path = file_path[1:]

        self.file_path = url_safe(file_path)
        self.url = url_safe(url)

    @property
    def posts(self):
        start = (self.page - 1) * self.posts_per_page
        end = start + self.posts_per_page
        return self._posts[start:end]

    @property
    def total(self):
        if self.posts_per_page == 0:
            return 1
        else:
            return int((len(self._posts)-1)/self.posts_per_page) + 1

    @property
    def next(self):
        if self.page == self.total:
            return None
        return Pagination(self._posts, self.page+1,
                self.base_url, self.posts_per_page)

    @property
    def prev(self):
        if self.page == 1:
            return None
        return Pagination(self._posts, self.page-1,
                self.base_url, self.posts_per_page)

    def iterate(self):
        curr = self
        for i in range(curr.page-1, self.total):
            yield curr
            curr = curr.next
