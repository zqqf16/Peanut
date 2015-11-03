#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from os.path import join, isdir, isfile, curdir

import peanut


DEFAULT_CONFIG = {
    'site': {
        'title': 'Peanut Demo',
        'url': 'http://peanut.zorro.im',
        'description': 'A simple static blog generator',
    },
    'author': {
        'image': 'https://avatars2.githubusercontent.com/u/655326?v=3&s=40',
        'name': 'zqqf16',
        'url': 'http://zorro.im/posts/about.html'
    },
    'path': {
        'draft': 'drafts',
        'post': 'posts/{slug}.html',
        'tag': 'tags/{slug}.html',
        'category': 'category/{slug}.html',
        'page': 'page/{slug}.html',
        'sitemap': 'sitemap.xml',
        'rss': 'rss.xml',
        'asset': '/asset/',
    },
    'sitemap': True,
    'rss': True,
    'theme': 'defult',
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
    post = 'post.html'
    index = 'index.html'

    # search in current dir
    local_path = join(curdir, theme)
    if isdir(local_path):
        if not isfile(join(local_path, post)):
            raise ValidationError('Template for post not found in theme {}'.format(theme))
        if not isfile(join(local_path, index)):
            raise ValidationError('Template for index not found in theme {}'.format(theme))

        # save theme path
        config.theme_path = local_path
        return

    # search in package
    package_path = os.path.split(peanut.__file__)[0]
    theme_path = join(package_path, 'themes', theme)
    if not isdir(theme_path):
        raise ValidationError('Theme named {} not found'.format(theme))

    config.theme_path = theme_path


def verify_path(config):
    """Verify path configurations"""

    draft = config.path['draft']
    if not isdir(draft):
        raise ValidationError('Draft path {} not found'.format(draft))


def verify_config(config):
    """Verify configurations"""

    verify_theme(config)
    verify_path(config)
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
