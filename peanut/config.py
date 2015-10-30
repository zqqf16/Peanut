#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs


DEFAULT_CONFIG = {
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


class Config(dict):
    """Configurations"""

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        return super(Config, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(Config, self).__getitem__(name)

    def __delitem__(self, name):
        return super(Config, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__


# Global config instance
config = Config(DEFAULT_CONFIG)


def _load_yaml(path):
    """Load config from YAML file
    """

    import yaml
    try:
        from yaml import CBaseLoader as Loader
    except ImportError:
        from yaml import BaseLoader as Loader

    with codecs.open(path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader)


def load(path):
    """Load config from file path
    """

    file_type = os.path.splitext(path)[1]
    if file_type.lower() in ('.yml', '.yaml'):
        config.update(_load_yaml(path))
