#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Writer"""

from __future__ import unicode_literals


import os
import six
import logging

from peanut.options import configs, env
from peanut.template import Template
from peanut.context import get_filters
from peanut.model import Tag, Post, Pagination


class Writer(object):
    """Base writer
    """

    def __init__(self, posts, template):
        self.posts = posts
        self.template = template

    def write_to_file(self, file_path, content):
        """Write content to file
        """

        file_path = os.path.join(configs.pwd, file_path)
        dirname = os.path.split(file_path)[0]
        try:
            logging.debug('Try to make directory %s', dirname, prefix='   ↳  ')
            os.makedirs(dirname)
        except OSError:
            pass

        with open(file_path, 'w') as f:
            if six.PY2:
                f.write(content.encode('utf-8'))
            else:
                f.write(content)
        f.close()

    def run(self):
        return NotImplemented


class PostWriter(Writer):
    """Post writer
    """

    def run(self):
        for post in self.posts:
            logging.debug('Render post %s', post.title)
            content = self.render(post)
            logging.debug('Write to %s', post.file_path, prefix='   ↳  ')
            self.write_to_file(post.file_path, content)

    def render(self, post):
        prev, next = self._get_post_naighbor(post)
        return self.template.render(post.layout, post=post,
                prev_post=prev, next_post=next)

    def _get_post_naighbor(self, post):
        """Get previous and next post
        """
        posts = self.posts
        index = posts.index(post)
        prev = None
        next = None
        if index > 0:
            prev = posts[index-1]
        if index < len(posts)-1:
            next = posts[index+1]

        return (prev, next)


class ArchiveWriter(Writer):
    """Archive writer"""

    def __init__(self, posts, template, layout=None, base_url=None):
        super(ArchiveWriter, self).__init__(posts, template)
        self.base_url = base_url or configs.path.index
        self.layout = layout or 'index'
        self.num_per_page = configs.pagination
        self.context = {}

    def run(self, posts=None):
        posts = posts or self.posts
        page = Pagination(posts, base_url=self.base_url,
                posts_per_page=self.num_per_page)

        for n, p in enumerate(page.iterate()):
            content = self.render(p)
            logging.debug('Write file %s', p.file_path, prefix='   ↳  ')
            self.write_to_file(p.file_path, content)

    def render(self, page):
        return self.template.render(self.layout, posts=page.posts, page=page,
                prev_page=page.prev, next_page=page.next, **self.context)


class TagWriter(ArchiveWriter):
    """Tag writer
    """

    def __init__(self, posts, template):
        super(TagWriter, self).__init__(posts, template, 'tag',
                configs.path.tag)
        self.tags = {}

        for p in posts:
            for tag in p.tags:
                if tag not in self.tags:
                    self.tags[tag] = [p]
                else:
                    self.tags[tag].append(p)

    def run(self):
        for tag in self.tags:
            logging.debug('Render tag %s', tag.title)
            posts = self.tags.get(tag)
            if not posts:
                continue
            self.context['tag'] = tag
            self.base_url = tag.file_path
            super(TagWriter, self).run(posts=posts)


class RssWriter(Writer):
    """Rss writer
    """
    def __init__(self, posts, template, layout='rss'):
        super(RssWriter, self).__init__(posts, template)
        self.file_path = configs.path[layout]
        self.layout = layout
        self.num = 5

    def run(self):
        logging.debug('Render %s', self.file_path)
        content = self.render()
        logging.debug('Write file %s', self.file_path)
        self.write_to_file(self.file_path, content)

    def render(self):
        return self.template.render(self.layout, posts=self.posts[:self.num])


class SitemapWriter(RssWriter):
    """Sitemap writer
    """
    def __init__(self, posts, template):
        super(SitemapWriter, self).__init__(posts, template, 'sitemap')
        self.num = len(self.posts)
