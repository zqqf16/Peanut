#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Markdown reader unittest
"""

from __future__ import unicode_literals

import unittest
import peanut.reader as pr


class TestMarkdown(unittest.TestCase):

    def test_parser(self):
        md_reader = pr.MarkdownReader()
        res = md_reader.read('drafts/example.md')
        self.assertEqual(res['title'], 'This is my title')
        self.assertEqual(res['html'], '<p>这行是中文</p>')
        self.assertEqual(res['slug'], 'example.md')
        self.assertIn('example', res['slug'])

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
