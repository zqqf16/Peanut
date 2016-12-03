#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import logging
import requests

logging.getLogger('requests').setLevel(logging.CRITICAL)
session = requests.session()

def api_path(url, path):
    return os.path.join(url, 'ghost/api/v0.1/', path)


def get_token(url, user, password):
    if not url or not user or not password:
        logging.error('Invalid url/username/password')
        return None

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = ('grant_type=password'
            '&username={}'
            '&password={}'
            '&client_id=ghost-admin'
            '&client_secret=8b4a248000cd').format(user, password)

    path = api_path(url, 'authentication/token')
    r = session.post(path, data=data, headers=headers)
    if r.status_code != 200:
        logging.error('Failed to get token, please check your username or password')
        return None

    return r.json()['access_token']


def post_to_json(post):
    date = post.date.strftime('%Y-%m-%dT%H:%M:%SZ')
    markdown = post.raw
    return {
        'status': 'published' if post.publish else 'draft',
        'title': post.title,
        'slug': post.slug,
        'markdown': post.raw,
        'image': post.image,
        'page': post.top,
        'language': "zh_CN",
        'meta_title': None,
        'meta_description': None,
        'author': 1,
        'created_at': date,
        'created_by': 1,
        #'updated_at': date,
        #'updated_by': 1,
        'published_at': date,
        'published_by': 1
      }


def push(url, token, posts):
    headers = {
        'Authorization': 'Bearer '+token,
        'Content-Type': 'application/json'
    }
    
    path = api_path(url, 'posts/')
    
    for post in posts:
        logging.info('Pushing %s', post.title, prefix='   ↳  ')
        posts_json = {'posts': [post_to_json(post)]}
        r = session.post(path, headers=headers, json=posts_json)
        if r.status_code != 201:
            logging.error('Push post failed, status code: {}, {}'.format(r.status_code, r.text))