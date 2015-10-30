#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import codecs

try:
    from yaml import CBaseLoader as Loader
except ImportError:
    from yaml import BaseLoader as Loader


class Config(object):
    """Site configure"""

    def __init__(self, path):
        configs = {}
        with codecs.open(path, 'r', encoding='utf-8') as f:
            configs = yaml.load(f.read(), Loader)
        self.title = configs.get('title')
        self.host = configs.get('host')
        self.description = configs.get('description')
        self.theme = configs.get('theme')
        self.path = configs.get('path')
