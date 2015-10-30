#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs


class Config(object):
    """Site configure"""

    def __init__(self, path):
        configs = Config.default_config()

        file_type = os.path.splitext(path)[1]
        if file_type.lower() in ('.yml', '.yaml'):
            configs.update(Config.__config_from_yaml(path))

        self.title = configs.get('title')
        self.host = configs.get('host')
        self.description = configs.get('description')
        self.theme = configs.get('theme')
        self.path = configs.get('path')

    @staticmethod
    def __config_from_yaml(path):
        """Load config from yaml file"""

        import yaml
        try:
            from yaml import CBaseLoader as Loader
        except ImportError:
            from yaml import BaseLoader as Loader

        with codecs.open(path, 'r', encoding='utf-8') as f:
            return yaml.load(f.read(), Loader)


    @staticmethod
    def default_config():
        return {
            'title': 'Peanut Demo',
            'host': 'peanut.zorro.im',
            'description': 'A simple static blog generator',
            'theme': 'defult',
            'path': {
                'draft': 'drafts',
                'target': 'posts',
                'sitemap': 'sitemap.xml',
                'rss': 'rss.xml',
            },
            'sitemap': True,
            'rss': True,
            'template': {
                'post': 'post.html',
                'tag': 'tag.html',
                'sitemap': 'sitemap.xml',
                'rss': 'rss.xml',
                'index': 'index.xml',
            }
        }
