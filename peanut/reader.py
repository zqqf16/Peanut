#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Markdown reader
"""

import os
import re
import codecs
import markdown

from six import with_metaclass
from peanut.meta_yaml import MetaYamlExtension


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

    def read(self, path):
        if not os.path.isfile(path):
            # is not a file
            return None

        file_name = os.path.basename(path)
        res = {'slug': file_name}

        with codecs.open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            html = self.parser.convert(content.strip(' \n'))

        res.update({'content': content, 'html': html})
        if self.md_parser.Meta:
            res.update(self.md_parser.Meta)

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
