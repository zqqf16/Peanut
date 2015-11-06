#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Markdown reader unittest
"""

from __future__ import unicode_literals

import unittest
import codecs

from datetime import datetime

import peanut.reader as pr


class TestMarkdown(unittest.TestCase):

    def setUp(self):
        md = '''\
---
title: Hello world
tags:
    - test
    - life
category: [test, useless]
publish: Yes
top: No
layout: post
date: 2015-11-5 16:56
cover: 'path/to/cover'
others:
    showTitle: Yes
---
我能吞下玻璃却不伤身体
'''
        with codecs.open('/var/tmp/test_markdown.md', 'w', encoding='utf-8') as f:
            f.write(md)

    def test_parser(self):
        reader = pr.MarkdownReader()
        draft = reader.read('/var/tmp/test_markdown.md')
        self.assertEqual(draft['meta']['publish'], True)
        self.assertEqual(draft['meta']['top'], False)
        self.assertEqual(draft['title'], 'Hello world')
        self.assertEqual(draft['content'], '<p>我能吞下玻璃却不伤身体</p>')
        self.assertIn('test', draft['meta']['tags'])
        self.assertIn('life', draft['meta']['tags'])
        self.assertEqual(draft['meta']['cover'], 'path/to/cover')
        self.assertDictEqual(draft['meta']['others'], {'showTitle': True})
        self.assertIn('test_markdown', draft['slug'])
        self.assertIsInstance(draft['meta']['date'], datetime)

    def test_get_reader(self):
        reader = None
        for name in ('a.md', 'a.MD', 'a.Markdown', 'a.markdown'):
            r = pr.reader_for_file(name)
            if not reader:
                reader = r
            self.assertIs(r, reader)

        r2 = pr.reader_for_file('b.unknow')
        self.assertIsNone(r2)


if __name__ == '__main__':
    unittest.main()
