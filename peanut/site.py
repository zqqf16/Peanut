#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import six
import shutil
import logging

import peanut
import peanut.reader as reader
import peanut.writer as writer

from peanut.model import Post
from peanut.options import configs, load_configs, verify_configs
from peanut.options import ValidationError
from peanut.template import Template
from peanut.context import get_filters
from peanut.utils import list_dir, get_resource

try:
    FileNotFoundError
except:
    FileNotFoundError = IOError


class Site(object):
    """Site"""

    default_config = ['_config.yaml', 'config.yaml',
            '_config.yml', 'config.yml']

    def __init__(self, directory='.'):

        logging.debug('Directory is {}'.format(directory))

        self.curdir = directory
        self.posts = []
        self.template = None

    @staticmethod
    def init(directory='./'):
        """Init peanut environments
        """
        # copy default config
        config_path = os.path.join(directory, 'config.yml')
        if os.path.isfile(config_path):
            logging.error('Config file %s already exists', config_path)
            return

        shutil.copy(get_resource('config.yml'), directory)
        logging.info('Config file created at %s', config_path, prefix='   ↳  ')

        # copy default theme assets
        assets_path = os.path.join(directory, 'assets/')
        if os.path.isdir(assets_path):
            logging.error('Asset directory %s alerady exists', assets_path)
            return

        shutil.copytree(get_resource('themes/default/assets'), assets_path)
        logging.info('Asset directory created at %s',
                assets_path, prefix='   ↳  ')

        # mkdir
        draft_path = os.path.join(directory, 'drafts/')
        if os.path.isdir(draft_path):
            logging.info('Draft directory already exists', prefix='   ↳  ')
            return
        try:
            os.makedirs(draft_path)
        except OSError:
            logging.error('Create draft directory failed')
        logging.info('Draft directory created at %s', draft_path,
                prefix='   ↳  ')


    def load_config(self, config_path):
        """Load config file from file
        """
        configs.pwd = self.curdir
        if not config_path:
            logging.debug('No config path is specified, try default ones')
            for file_name in self.default_config:
                p = os.path.join(self.curdir, file_name)
                if os.path.isfile(p):
                    logging.debug('Find config file named %s', file_name)
                    config_path = file_name
                    break
            else:
                logging.debug('Config file with default names not found')
                raise FileNotFoundError('Config file not found at directory \
{}'.format(self.curdir))
        else:
            if not os.path.isfile(os.path.join(self.curdir, config_path)):
                logging.debug('%s is not a file', config_path)
                raise FileNotFoundError('Config file not found at path {}'\
                        .format(config_path))

        logging.debug('Load config file {}'.format(config_path))
        load_configs(config_path)

        logging.info('Verifing configurations...')
        verify_configs()

        self.template = Template(
                configs.theme_path,
                filters=get_filters(configs),
                site=configs.site,
                author=configs.author)

    def load_drafts(self):
        """Load all drafts
        """
        draft_dir = os.path.join(configs.pwd, configs.path.draft)
        for f in list_dir(draft_dir):
            logging.visiable('Reading {}'.format(f))
            self.parse_draft(f)

    def parse_draft(self, draft_file):
        """Parse draft file
        """
        draft = reader.read(draft_file)
        if not draft:
            logging.visiable('Failed', prefix='   ✗  ')
            return

        title = draft.get('title', None)
        slug = draft.get('slug', None)
        if not title or not slug:
            logging.visiable('✗ No title or slug', prefix='   ↳  ')
            return

        if not draft['meta'].get('publish', True):
            logging.visiable('✗ Don\'t publish', prefix='   ↳  ')
            return

        post = Post(title, slug, draft.get('content', None),
                draft.get('meta', None))

        self.posts.append(post)
        logging.visiable('✓ %s', post.title, prefix='   ↳  ')


    def generate(self):
        """Generate static site
        """
        logging.info('Loading drafts...')
        self.load_drafts()
        self.posts.sort(reverse=True)

        writers = [
            (writer.PostWriter, 'posts'),
            (writer.TagWriter, 'tags'),
            (writer.ArchiveWriter, 'index'),
        ]

        if configs.rss:
            writers.append((writer.RssWriter, 'rss'))
        if configs.sitemap:
            writers.append((writer.SitemapWriter, 'sitemap'))

        logging.info('Rendering files...')
        for writer_class, desp in writers:
            logging.visiable(desp)
            w = writer_class(posts=self.posts, template=self.template)
            w.run()

        logging.info('%d posts', len(self.posts),
                prefix='🍻  ')
