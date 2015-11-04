#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Markdown reader
"""

import os
import re
import codecs
import markdown

from datetime import datetime
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
    date_string = parser_single(value)
    date = datetime.now()
    for date_format in ['%Y-%m-%d', '%Y%m%d', '%Y-%m-%d %H:%M', '%Y%m%d %H:%M']:
        try:
            date = datetime.strptime(date_string, date_format)
        except ValueError:
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
            parser = self._meta_parser.get(key, parser_single)
            new_meta[key] = parser(value)
        return new_meta

    def read(self, path):
        if not os.path.isfile(path):
            # is not a file
            return None

        file_name = os.path.basename(path)
        res = {'slug': file_name}

        with codecs.open(path, 'r', encoding='utf-8') as f:
            draft = f.read()
            content = self.parser.convert(draft.strip(' \n'))

        res.update({'content': content, 'draft': draft})
        if self.md_parser.Meta:
            res.update(self.parse_meta(self.md_parser.Meta))

        return res


def reader_for_file(path):
    """Get the reader instance for file path
    """

    file_name = os.path.basename(path)
    for cls in Reader.__subclasses__():
        if cls.regex and cls.regex.match(file_name):
            return cls()

    return None


def read(path):
    """Read file at path
    """

    reader = reader_for_file(path)
    if not reader:
        return None

    return reader.read(path)
