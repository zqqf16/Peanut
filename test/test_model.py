#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Model unittest
"""

from __future__ import unicode_literals

import unittest
from peanut.model import Post, Tag, Category


class TestModel(unittest.TestCase):
    def test_base_model(self):
        tag = Tag('test')
        self.assertEqual(tag.title, 'test')
        self.assertEqual(tag.slug, 'test')
        self.assertListEqual(list(tag.posts), [])
        self.assertEqual(tag.url, '/tags/test.html')
        self.assertEqual(tag.file_path, 'tags/test.html')

    def test_relationship(self):
        post = Post.create('Hello world', 'hello_world')
        tag = Tag.create('test')
        category = Category.create('test')

        post.add_tag(tag)
        post.category = category

        self.assertIn(tag, post.tags)
        self.assertIn(post, list(tag.posts))
        self.assertIn(post, list(category.posts))
        self.assertIs(post.category, category)

        category_new = Category.create('test_again')
        post.category = category_new

        self.assertIs(post.category, category_new)
        self.assertListEqual(list(category.posts), [])


    def test_post(self):
        post_a = Post.create('Post a', 'post_a', top=False, publish=True)
        post_b = Post.create('Post b', 'post_b', top=True, publish=False)
        self.assertListEqual(list(Post.all(lambda p: p.top)), [post_b])
