#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import six

import peanut
import peanut.reader as reader
import peanut.writer as writer

from peanut.model import Post
from peanut.options import configs, env, load_configs
from peanut.template import Template
from peanut.context import get_filters
from peanut.utils import list_dir


class Site(object):
    """Site"""

    default_config = ['_config.yaml', 'config.yaml',
            '_config.yml', 'config.yml']

    def __init__(self, directory='.', config_path=None):
        self.curdir = directory
        self.load_config(config_path)
        self.posts = []
        self.template = Template(
                configs.theme_path,
                filters=get_filters(configs),
                site=configs.site,
                author=configs.author)

    def load_config(self, config_path):
        """Load config file from file
        """
        configs.pwd = self.curdir
        if not config_path:
            for file_name in self.default_config:
                p = os.path.join(self.curdir, file_name)
                if os.path.isfile(p):
                    config_path = file_name
                    break
            else:
                raise FileNotFoundError('Config file not found at directory \
{}'.format(self.curdir))
        else:
            if not os.path.isfile(os.path.join(self.curdir, config_path)):
                raise FileNotFoundError('Config file not found at path {}'\
                        .format(config_path))

        load_configs(config_path)


    def load_drafts(self):
        """Load all drafts
        """
        draft_dir = os.path.join(configs.pwd, configs.path.draft)
        for f in list_dir(draft_dir):
            if f.startswith('.'):
                continue
            self.parse_draft(f)


    def parse_draft(self, draft_file):
        """Parse draft file
        """
        draft = reader.read(draft_file)
        if not draft:
            return
        if not draft.get('publish', True):
            return

        title = draft.get('title', None)
        slug = draft.get('slug', None)
        if not title or not slug:
            return

        post = Post(title, slug, draft.get('content', None),
                draft.get('meta', None))
        self.posts.append(post)


    def generate(self):
        """Generate static site
        """
        self.load_drafts()

        writers = [
            writer.PostWriter,
            writer.TagWriter,
            writer.ArchiveWriter,
        ]

        if configs.rss:
            writers.append(writer.RssWriter)
        if configs.sitemap:
            writers.append(writer.SitemapWriter)

        for writer_class in writers:
            w = writer_class(posts=self.posts, template=self.template)
            w.run()
