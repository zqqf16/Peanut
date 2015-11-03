#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Model unittest
"""

from __future__ import unicode_literals

import unittest
from peanut.model import Post, Tag, Category


class TestModel(unittest.TestCase):
    def test_pool(self):
        tag_a = Tag('hello')
        tag_b = Tag('hello')

        self.assertIs(tag_a, tag_b)

    def test_base_model(self):
        tag = Tag('test')
        self.assertEqual(tag.title, 'test')
        self.assertEqual(tag.slug, 'test')
        self.assertEqual(tag.posts, [])
        self.assertEqual(tag.url, 'tags/test.html')
