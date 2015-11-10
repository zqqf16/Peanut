#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Markdown reader
"""

from __future__ import unicode_literals

import os
import six
import re
import markdown
import datetime
import logging

from six import with_metaclass
from peanut.meta_yaml import MetaYamlExtension


def parser_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]

def parser_single(value):
    if isinstance(value, list):
        return value[0]
    else:
        return value

def parser_bool(value):
    value = parser_single(value)
    if isinstance(value, bool):
        return value
    if value in ['True', 'true', 'Yes', 'yes']:
        return True
    else:
        return False

def parser_date(value):
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime(value.year, value.month, value.day)

    date_string = parser_single(value)
    date = datetime.datetime.now()
    for date_format in ['%Y-%m-%d', '%Y%m%d', '%Y-%m-%d %H:%M', '%Y%m%d %H:%M']:
        try:
            date = datetime.datetime.strptime(date_string, date_format)
        except:
            pass
    return date


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Reader(object):
    """Base reader class
    """

    regex = None

    def read(self, path):
        '''Read file'''
        return NotImplemented


class MarkdownReader(with_metaclass(Singleton, Reader)):
    """Markdown reader
    """

    regex = re.compile(r'([^/]+)\.(MD|md|[mM]arkdown)')

    # Meta data parser
    _meta_parser = {
        'tags': parser_list,
        'category': parser_single,
        'date': parser_date,
        'publish': parser_bool,
        'top': parser_bool,
        'image': parser_single,
    }

    def __init__(self):
        self.md_parser = MarkdownReader.__create_md_reader()

    @classmethod
    def __create_md_reader(cls):
        """Create markdown parser
        """

        extensions = [
            'markdown.extensions.fenced_code',  # Fenced Code Blocks
            'markdown.extensions.codehilite',   # CodeHilite
            'markdown.extensions.footnotes',    # Footnotes
            'markdown.extensions.tables',       # Tables
            'markdown.extensions.smart_strong', # Smart Strong
            'markdown.extensions.toc',          # Table of Contents
            MetaYamlExtension(),                # Meta-YAML
        ]

        # Do not guess the code language
        extension_configs = {'codehilite': [('guess_lang', False)]}

        return markdown.Markdown(extensions=extensions,
                                 extension_configs=extension_configs)

    @property
    def parser(self):
        return self.md_parser.reset()

    def parse_meta(self, meta):
        new_meta = {}
        for key, value in meta.items():
            parser = self._meta_parser.get(key, lambda v: v)
            new_meta[key] = parser(value)
        return new_meta

    def read(self, path):
        if not os.path.isfile(path):
            # is not a file
            return None

        file_name = os.path.basename(path).split('.')[0]
        res = {'slug': file_name}

        with open(path, 'r') as f:
            draft = f.read()
            if six.PY2:
                draft = draft.decode('utf-8')
            content = self.parser.convert(draft.strip(' \n'))

        res.update({'content': content, 'draft': draft})
        if self.md_parser.Meta:
            new_meta = self.parse_meta(self.md_parser.Meta)
            res['title'] = new_meta.pop('title')
            res['meta'] = new_meta

        return res


def reader_for_file(path):
    """Get the reader instance for file path
    """

    file_name = os.path.basename(path)
    for cls in Reader.__subclasses__():
        if cls.regex and cls.regex.match(file_name):
            logging.debug('Find reader {}'.format(cls))
            return cls()

    return None


def read(path):
    """Read file at path
    """

    reader = reader_for_file(path)
    if not reader:
        logging.debug('No reader found for file %s', path)
        return None

    return reader.read(path)
