#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from os.path import join, isdir, isfile, curdir

import peanut


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


class ValidationError(Exception):
    """Configurations validation exception"""
    pass


def verify_theme(config):
    """Verify theme configurations"""

    theme = config.theme
    post = config.template['post']
    index = config.template['index']

    # search in current dir
    local_path = join(curdir, theme)
    if isdir(local_path):
        if not isfile(join(local_path, post)):
            raise ValidationError('Template for post not found in theme {}'.format(theme))
        if not isfile(join(local_path, index)):
            raise ValidationError('Template for index not found in theme {}'.format(theme))
        return

    # search in package
    package_path = os.path.split(peanut.__file__)[0]
    theme_path = join(package_path, 'templates', theme)
    if not isdir(theme_path):
        raise ValidationError('Theme named {} not found'.format(theme))


def verify_config(config):
    """Verifying configurations"""

    verify_theme(config)
    # TODO: other configs


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

    verify_config(config)
