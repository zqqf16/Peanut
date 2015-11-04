#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import peanut.reader as reader
from peanut.config import config
from peanut.model import Tag, Category, Post
from peanut.template import Template
from peanut.context import filters
from peanut.utils import neighborhood

def render_post(template, post):
    template.render(post.layout, post=post)
    pass

def render_tag(template, tag):
    pass

def render_category(template, category):
    pass

def render_static_files(template, static_file):
    pass

def generate():
    """Generate all site files"""

    context = {
        'site': config.site,
        'author': config.author,
    }

    template = Template(config.theme_path, filters=filters, **context)

    #posts
    for prev, post, next in neighborhood(Post.all()):
        template.render(post.layout, post=post, prev_post=prev, next_post=next)


def create_post(draft):
    """Create post with draft"""

    if not draft.get('title') or not draft.get('slug'):
        return

    Post.create(**draft)

    if draft.get('tags'):
        for tag in draft['tags']:
            Tag.create(tag)
    if draft.get('catetory'):
        for category in draft['category']:
            Category.create(category)


def read_all_drafts(path):
    """Read all drafts from path"""

    for f in os.listdir(path):
        if f.startswith('.'):
            continue

        p = os.path.join(path, f)
        if os.path.isdir(p):
            read_all_drafts(p)
            continue

        draft = reader.read(p)
        if draft:
            create_post(draft)


def start(directory='.', config_path=None):
    """Start loading drafts and generationg HTML files"""

    config.curdir = directory
    if config_path:
        if not os.path.isfile(config_path):
            raise FileNotFoundError('Config file not found at path {}'\
                    .format(config_path))
        config.load(config_path)

    draft_path = os.path.join(directory, config.path.draft)
    read_all_drafts(draft_path)

    generate()
