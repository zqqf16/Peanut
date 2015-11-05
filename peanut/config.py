#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from os.path import join, isdir, isfile, curdir

import peanut


class ValidationError(Exception):
    """Configurations validation exception"""
    pass


class Config(dict):
    """Configurations"""

    def __init__(self, *args, **kwargs):
        self.curdir = curdir
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = Config(value)
        return super(Config, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(Config, self).__getitem__(name)

    def __delitem__(self, name):
        return super(Config, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def __real_update(self, key, value):
        if self.get(key) and isinstance(self[key], Config):
            if isinstance(value, dict):
                value = Config(value)
            if isinstance(value, Config):
                self[key].update(value)
            else:
                self[key] = value
        else:
            self[key] = value

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError('update expected at most 1 arguments, got {}'\
                .format(len(args)))
            arg = dict(args[0])
            for key, value in arg.items():
                self.__real_update(key, value)

        for key, value in kwargs.items():
            self.__real_update(key, value)

    def _read_yaml(self, config_path):
        """Load config from YAML file
        """

        import yaml

        with codecs.open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load(self, config_path):
        """Load config from config_path"""

        file_type = os.path.splitext(config_path)[1]
        if file_type.lower() in ('.yml', '.yaml'):
            self.update(self._read_yaml(config_path))
        else:
            return

        self.verify()
        return self

    def verify(self):
        """Verify configurations"""
        self.verify_path()
        self.verify_theme()

    def verify_path(self):
        """Verify path configurations"""

        draft = join(self.curdir, self.path.draft)
        if not isdir(draft):
            raise ValidationError('Draft path {} not found'.format(draft))

    def verify_theme(self):
        """Verify theme configurations"""

        theme = self.theme
        post = 'post.html'
        index = 'index.html'

        # search in current dir
        local_path = join(self.curdir, theme)
        if isdir(local_path):
            if not isfile(join(local_path, post)):
                raise ValidationError('Template for post not found in theme {}'\
                        .format(theme))
            if not isfile(join(local_path, index)):
                raise ValidationError('Template for index not found in theme {}'\
                        .format(theme))

            # save theme path
            self.theme_path = local_path
            return

        # search in package
        package_path = os.path.split(peanut.__file__)[0]
        theme_path = join(package_path, 'themes', theme)
        if not isdir(theme_path):
            raise ValidationError('Theme named {} not found'.format(theme))

        self.theme_path = theme_path


# Global config instance
def default_config():
    return Config({
            'site': {
                'title': 'Peanut Demo',
                'logo': 'path_to_your_logo',
                'cover': None,
                'url': 'http://peanut.zorro.im',
                'description': 'A simple static blog generator',
                'navigation': False,
            },
            'author': {
                'image': 'https://avatars2.githubusercontent.com/u/655326?v=3&s=40',
                'name': 'zqqf16',
                'url': 'http://zorro.im/posts/about.html',
                'bio': 'Pythoner',
                'location': 'Beijing',
                'website': 'http://zorro.im',
            },
            'path': {
                'draft': 'drafts',
                'post': 'posts/{slug}.html',
                'tag': 'tags/{slug}.html',
                'category': 'category/{slug}.html',
                'page': 'page/{slug}.html',
                'index': 'index.html',
                'sitemap': 'sitemap.xml',
                'rss': 'rss.xml',
                'asset': '/assets/',
            },
            'sitemap': True,
            'rss': True,
            'theme': 'default',
    })
