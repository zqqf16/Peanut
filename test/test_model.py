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
        self.assertEqual(tag_a.title, 'hello')
        self.assertEqual(tag_a.slug, 'hello')
        self.assertEqual(tag_a.posts, [])
