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

    def test_relationship(self):
        post = Post('Hello world', 'hello_world')
        tag = Tag('test')
        category = Category('test')

        tag.add_post(post)
        post.add_tag(tag)

        category.add_post(post)
        post.category = category

        self.assertIn(tag, post.tags)
        self.assertIn(post, tag.posts)
        self.assertIn(post, category.posts)
        self.assertIs(post.category, category)
