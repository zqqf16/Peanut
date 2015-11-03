#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import utils
import config

from reader import Reader
from model import Post, Category, Tag

class Blog(object):

    def __init__(self):
        self.posts = []
        self.categories = {}
        self.tags = {}
        self._tag_titles = {}

        self.reader = Reader()

    def load(self):
        draft_path = config.path['drafts']

        tree = utils.walk_directory(draft_path)

        for n, d in tree['dirs'].items():
            title = os.path.split(n)[1]
            category = Category(title=title)
            posts = []

            # Do not support sub category.
            for f in d['files']:
                posts.append(self._process_file(f, category))

            self.categories[category] = posts
            self.posts += posts

        for f in tree['files']:
            post = self._process_file(f)
            if post:
                self.posts.append(post)

    def _process_file(self, path, category=None):
        '''Read file, create post and tags'''

        draft = self.reader.read(path)
        if not draft:
            # TODO
            return

        tags = [self._get_tag(t) for t in draft['tags']]
        draft['tags'] = tags

        post = Post(category=category, **draft)

        #Set tag
        for t in tags:
            self.tags[t].append(post)

        return post

    def _get_tag(self, title):
        '''Get a tag from self.tags if it exists, else create a new one'''

        t = self._tag_titles.get(title)
        if t:
            return t

        tag = Tag(title)
        self.tags[tag] = []
        self._tag_titles[title] = tag

        return tag
