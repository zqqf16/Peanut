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
        self.assertEqual(res['publish'], True)
        self.assertEqual(res['top'], False)
        self.assertEqual(res['title'], 'This is my title')
        self.assertEqual(res['content'], '<p>这行是中文</p>')
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

    def test_meta_parser(self):
        self.assertEqual(pr.parser_single('hello'), 'hello')
        self.assertEqual(pr.parser_single(['hello', 'world']), 'hello')

        self.assertListEqual(pr.parser_list('hello'), ['hello'])
        self.assertListEqual(pr.parser_list(['hello', 'world']),
                ['hello', 'world'])

        for value in ['Yes', 'yes', 'true', 'True', True]:
            self.assertTrue(pr.parser_bool(value))
        for value in ['No', 'no', 'false', 'False', False]:
            self.assertFalse(pr.parser_bool(value))



if __name__ == '__main__':
    unittest.main()
