#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Model unittest
"""

from __future__ import unicode_literals

import unittest
from datetime import datetime
from peanut.model import Post, Tag, Pagination
from peanut.options import configs, env


class TestPost(unittest.TestCase):
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

        post2 = Post('1', '1', '')
        post2.date = datetime.now()
        self.assertTrue(post < post2)

    def test_relationships(self):
        tags=['test', 'relation']
        t1 = Tag(tags[0])
        t2 = Tag(tags[1])

        p = Post('Hello world', 'hello-world', 'content', meta={'tags': tags})

        self.assertIn(t1, p.tags)
        self.assertIn(t2, p.tags)

class TestPagination(unittest.TestCase):
    def test_pagination(self):
        posts = []
        for i in range(0, 10):
            title = 'post_{}'.format(i)
            posts.append(Post(title, title, title))

        page = Pagination(posts, base_url='tags/test/', posts_per_page=2)

        self.assertEqual(page.page, 1)
        self.assertEqual(page.total, 5)
        self.assertListEqual(page.posts, posts[0:2])

        self.assertIsNone(page.prev)

        next = page.next
        self.assertListEqual(next.posts, posts[2:4])

        n = 0
        for p in page.iterate():
            self.assertEqual(p.page, n+1)
            self.assertListEqual(p.posts, posts[n*2:n*2+2])
            n += 1

    def test_path(self):
        posts = []
        for i in range(0, 10):
            title = 'post_{}'.format(i)
            posts.append(Post(title, title, title))

        page = Pagination(posts, base_url='/tags/test')
        self.assertEqual(page.url, '/tags/test/')
        self.assertEqual(page.file_path, 'tags/test/index.html')

        page = Pagination(posts, base_url='/tags/test/index.html',).next
        self.assertEqual(page.url, '/tags/test/page/2/index.html')
        self.assertEqual(page.file_path, 'tags/test/page/2/index.html')
