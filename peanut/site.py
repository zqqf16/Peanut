#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

import peanut
import peanut.reader as reader
from peanut.model import SinglePage, Tag, Category, Post
from peanut.config import default_config
from peanut.template import Template
from peanut.context import get_filters


class Site(object):
    """Site"""

    default_config = ['_config.yaml', 'config.yaml',
            '_config.yml', 'config.yml']

    def __init__(self, directory='.', config_path=None):
        self.curdir = directory
        self.config = self.load_config(config_path)

        self.template = Template(
                self.config.theme_path,
                filters=get_filters(self.config),
                site=self.config.site,
                author=self.config.author)

    @property
    def posts(self):
        return Post.all()

    @property
    def tags(self):
        return Tag.all()

    @property
    def categories(self):
        return Category.all()

    @property
    def single_pages(self):
        return SinglePage.all()

    @property
    def get_file_path(self, item):
        template = self.config.path[item.layout]
        if not template:
            raise KeyError('Path for {} not found'.format(item.layout))

        return template.format(**item.__dict__)

    def load_config(self, config_path):
        """Load config file from file
        """
        config = default_config()
        config.curdir = self.curdir

        if not config_path:
            for file_name in self.default_config:
                p = os.path.join(self.curdir, file_name)
                if os.path.isfile(p):
                    config_path = p
                    break
            else:
                raise FileNotFoundError('Config file not found at directory \
{}'.format(self.curdir))
        else:
            if not os.path.isfile(config_path):
                raise FileNotFoundError('Config file not found at path {}'\
                        .format(config_path))

        config.load(config_path)

        Post.path_template = config.path.post
        Tag.path_template = config.path.tag
        Category.path_template = config.path.category

        return config

    def load_drafts(self):
        """Load all drafts
        """
        draft_dir = os.path.join(self.curdir, self.config.path.draft)
        for f in os.listdir(draft_dir):
            if f.startswith('.'):
                continue
            p = os.path.join(draft_dir, f)
            self.parse_draft(p)

        # Create index, rss and sitemap
        for page in ('index', 'rss', 'sitemap'):
            single_page = SinglePage.create(page, page)
            single_page.layout = page
            single_page.path_template = self.config.path[page]


    def parse_draft(self, draft_file):
        """Parse draft file
        """
        draft = reader.read(draft_file)
        if not draft:
            return

        if not draft.get('title') or not draft.get('slug'):
            return

        if not draft.get('publish', True):
            return

        Post.create(**draft)

        if draft.get('tags'):
            for tag in draft['tags']:
                Tag.create(tag)
        if draft.get('catetory'):
            for category in draft['category']:
                Category.create(category)

    def _get_post_naighbor(self, post):
        """Get previous and next post
        """
        posts = self.posts
        index = posts.index(post)
        prev = None
        next = None
        if index > 0:
            prev = posts[index-1]
        if index < len(posts)-1:
            next = posts[index+1]

        return (prev, next)

    def render_post(self, post):
        """Render post
        """
        prev, next = self._get_post_naighbor(post)
        return self.template.render(post.layout, post=post,
                prev_post=prev, next_post=next)

    def render_tag(self, tag):
        """Render tag
        """
        return self.template.render(tag.layout, tag=tag, posts=tag.posts)

    def render_category(self, category):
        """Render category
        """
        return self.template.render(category.layout, category=category,
                posts=category.posts)

    def render_single_page(self, page):
        """Render single page
        """
        return self.template.render(page.layout, posts=self.posts)

    def write_html(self, item, content):
        """Write HTML file"""

        path = os.path.join(self.config.curdir, item.file_path)
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        with codecs.open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate(self):
        """Generate static site
        """
        self.load_drafts()
        for post in self.posts:
            content = self.render_post(post)
            self.write_html(post, content)
        for tag in self.tags:
            content = self.render_tag(tag)
            self.write_html(tag, content)
        for category in self.categories:
            content = self.render_category(category)
            self.write_html(category, content)
        for page in self.single_pages:
            content = self.render_single_page(page)
            self.write_html(page, content)
