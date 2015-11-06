#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Writer"""

import os
import six

from peanut.options import configs, env
from peanut.template import Template
from peanut.context import get_filters
from peanut.model import Tag, Post, Pagination


"""
template = Template(
    configs.theme_path,
    filters=get_filters(configs),
    site=configs.site,
    author=configs.author
)
"""

class Writer(object):
    """Base writer
    """

    def __init__(self, posts, template):
        self.posts = posts
        self.template = template

    def write_to_file(self, file_path, content):
        """Write content to file
        """
        dirname = os.path.split(file_path)[0]
        try:
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
            content = self.render(post)
            self.write_to_file(post.file_path, content)

    def render(self, post):
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

    def __init__(self, posts, layout=None, base_url=None):
        super(ArchiveWriter, self).__init__(posts)
        self.base_url = base_url or configs.path.index
        self.layout = layout or 'index'
        self.num_per_page = configs.pagination

    def run(self, posts=None):
        posts = posts or self.posts
        page = Pagination(posts, base_url=self.base_url,
                posts_per_page=self.num_per_page)

        for n, p in enumerate(page.iterate()):
            content = self.render(p)
            self.write_to_file(p.file_path, content)

    def render(self, page):
        return self.template.render(self.layout, posts=page.posts,
                prev_page=page.prev, next_page=page.next)


class TagWriter(ArchiveWriter):
    """Tag writer
    """

    def __init__(self, posts):
        super(TagWriter, self).__init__(posts, 'tag', config.path.tag)
        self.tags = {}

        for p in posts:
            for tag in p.tags:
                if tag not in self.tags:
                    self.tags[tag] = [p]
                else:
                    self.tags[tag].append(p)

    def run(self):
        for tag in self.tags:
            posts = self.tags.get(tag)
            if not posts:
                continue
            super(TagWriter, self).run(posts=posts)


class RssWriter(ArchiveWriter):
    """Rss writer
    """
    def __init__(self, posts):
        super(RssWriter, self).__init__(posts, 'rss', config.path.rss)


class SitemapWriter(ArchiveWriter):
    """Sitemap writer
    """
    def __init__(self, posts):
        super(SitemapWriter, self).__init__(posts, 'sitemap',
                config.path.sitemap)
