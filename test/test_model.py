#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Model unittest
"""

from __future__ import unicode_literals

import unittest
from datetime import datetime
from peanut.model import Post, Tag
from peanut.options import configs, env


class TestModel(unittest.TestCase):
    def test_post(self):
        meta = {
            'date': None,
            'tags': ['hello', 'world'],
            'layout': None,
            'top': True,
            'publish': False,
            'author': 'zqqf16',
        }
        post = Post('Hello world', 'hello_world', 'Hello world', meta)

        now = datetime.now()

        self.assertEqual(post.title, 'Hello world')
        self.assertEqual(post.slug, 'hello_world')
        self.assertEqual(post.author, 'zqqf16')
        self.assertEqual(post.date.year, now.year)
        self.assertTrue(post.top)
        self.assertFalse(post.publish)

        configs.path.post = 'posts/{slug}.html'
        self.assertEqual(post.file_path, 'posts/hello_world.html')
        self.assertEqual(post.url, '/posts/hello_world.html')

        configs.path.post = 'posts/{title}.html'
        self.assertEqual(post.file_path, 'posts/Hello-world.html')
        self.assertEqual(post.url, '/posts/Hello-world.html')

    def test_relationships(self):
        tags=['test', 'relation']
        t1 = Tag(tags[0])
        t2 = Tag(tags[1])

        p = Post('Hello world', 'hello-world', 'content', meta={'tags': tags})

        self.assertIn(t1, p.tags)
        self.assertIn(t2, p.tags)
