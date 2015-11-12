#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import codecs
import yaml
import logging

import peanut


class ValidationError(Exception):
    """Configs validation exception"""
    def __init__(self, msg=None):
        super(ValidationError, self).__init__(msg)
        self.msg = msg

class LoadingError(ValidationError):
    """Loading exception"""
    pass


class Option(dict):
    """Optionurations"""

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = Option(value)
        return super(Option, self).__setitem__(key, value)

    def __getitem__(self, name):
        try:
            return super(Option, self).__getitem__(name)
        except KeyError:
            return None

    def __delitem__(self, name):
        return super(Option, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def __real_update(self, key, value):
        if self.get(key) and isinstance(self[key], Option):
            if isinstance(value, dict):
                value = Option(value)
            if isinstance(value, Option):
                self[key].update(value)
            else:
                self[key] = value
        else:
            self[key] = value

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError(
                        'update expected at most 1 arguments, got {}'\
                        .format(len(args)))
            arg = dict(args[0])
            for key, value in arg.items():
                self.__real_update(key, value)

        for key, value in kwargs.items():
            self.__real_update(key, value)

# Default site configurations
configs = Option({
    'pwd': os.getcwd(),
    'site': {
        'title': 'Peanut',
        'logo': None,
        'cover': None,
        'url': 'http://peanut.zorro.im',
        'description': 'Another peanut blog',
        'navigation': False,
    },
    'author': {
        'image': None,
        'name': 'Your Name',
        'url': '/posts/about.html',
        'bio': None,
        'location': 'Beijing, China',
    },
    'path': {
        'draft': 'drafts',
        'post': 'posts/{slug}.html',
        'tag': 'tags/{title}/',
        'pagination': 'page/{num}/',
        'index': 'index.html',
        'sitemap': 'sitemap.xml',
        'rss': 'rss.xml',
        'asset': '/assets/',
    },
    'sitemap': True,
    'rss': True,
    'theme': 'default',
    'theme_path': '',
    'pagination': 10,
})


def verify_path():
    """Verify path configurations"""

    draft = os.path.join(configs.pwd, configs.path.draft)
    if not os.path.isdir(draft):
        raise ValidationError('Draft path {} not found'.format(draft))
    site_url = configs.site.url
    if not site_url.startswith('http'):
        configs.site.url = 'http://'+site_url

def verify_theme():
    """Verify theme configurations"""

    theme = configs.theme
    post = 'post.html'
    index = 'index.html'

    # search in current dir
    local_path = os.path.join(configs.pwd, theme)
    if os.path.isdir(local_path):
        for template in (post, index):
            if not os.path.isfile(os.path.join(local_path, template)):
                raise ValidationError('Template for {} not found in'
                        'theme {}'.format(template, theme))

        # save theme path
        configs.theme_path = local_path
        return

    # search in package
    package_path = os.path.abspath(os.path.split(__file__)[0])
    theme_path = os.path.join(package_path, 'themes', theme)
    if not os.path.isdir(theme_path):
        raise ValidationError('Theme named {} not found'.format(theme))

    # update theme_path
    configs.theme_path = theme_path

def verify_configs():
    for verify_func in (verify_path, verify_theme):
        verify_func()

def load_yaml(path):
    """Load YAML format config file
    """
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_configs(path):
    """Load configs from path
    """
    file_type = os.path.splitext(path)[1]
    abs_path = os.path.join(configs.pwd, path)
    if file_type.lower() in ('.yml', '.yaml'):
        config_yaml = load_yaml(abs_path)
        if config_yaml:
            configs.update(config_yaml)
        else:
            logging.debug('Config file is empty')
    else:
        raise LoadingError('Unsupported config file type {}'.format(file_type))

# Global environments

env = Option({
    'posts': [],
})
