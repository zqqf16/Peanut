#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Post, Tag and Category
"""

import inspect

from six import with_metaclass
from datetime import datetime

from peanut.config import config


class ObjectPool(type):
    """Meta class to implement a simple "object pool".
    """

    def __new__(mcs, name, bases, attrs):
        """Add an attribute "_pool".
        """
        attrs['_pool'] = {}
        return super(ObjectPool, mcs).__new__(mcs, name, bases, attrs)


class BaseModel(with_metaclass(ObjectPool, object)):
    """Base model"""

    # Pool identity key
    _identity = 'title'

    # layout
    layout = 'page'

    @classmethod
    def all(cls):
        """Get all instance from pool"""
        return cls._pool.values()

    @classmethod
    def get(cls, identity):
        """Get an instance from pool by identity"""
        return cls._pool.get(identity)

    @classmethod
    def create(cls, *args, **kwargs):
        """Create an instance"""
        instance = cls(*args, **kwargs)
        cls._pool[instance.identity] = instance
        return instance

    @classmethod
    def get_or_create(cls, *args, **kwargs):
        """Get an instance from pool, if does not exist, create a new one"""
        id_key = getattr(cls, '_identity', None)
        call_args = inspect.getcallargs(cls.__init__, None, *args, **kwargs)
        identity = call_args.get(id_key)
        instance = cls.get(identity, None)
        return instance or cls.create(*args, **kwargs)

    @classmethod
    def add(cls, instance):
        cls._pool[instance.identity] = instance

    @property
    def identity(self):
        return self.__dict__[self._identity]

    def __init__(self, title, slug):
        self.title = title
        self.slug = slug

    @property
    def url(self):
        path = config.path[self.layout]
        if not path:
            raise KeyError('Path for {} not found'.format(self.layout))
        return path.format(**self.__dict__)


class Post(BaseModel):
    '''Post'''

    layout = 'post'

    def __init__(self, title, slug, content=None, date=None,
                 publish=True, top=False, layout='post',
                 tags=None, category=None, **kwargs):

        super(Post, self).__init__(title=title, slug=title)

        self.content = content
        self.date = date or datetime.now()
        self.top = top
        self.publish = publish
        self.layout = layout
        self._tags = set()
        self._category = None

        if tags:
            for tag in tags:
                self.add_tag(tag)

        if category:
            self.category = category

    def add_tag(self, tag):
        """Add tag"""
        self._tags.add(tag.title)

    @classmethod
    def all(cls, post_filter=None):
        """Get all posts
        @param post_filter: a callable filter
        @return: post list
        """
        return filter(post_filter, super(Post, cls).all())

    @classmethod
    def top_posts(cls):
        """Get all top posts"""
        return filter(lambda p: p.top, cls.all())

    @property
    def tags(self):
        """Get all tags"""
        return [Tag.get(tag) for tag in self._tags]

    @property
    def catetory(self):
        return Category.get(self._category)

    @catetory.setter
    def category(self, value):
        if value:
            self._category = value.title
        else:
            self._category = None


class Tag(BaseModel):
    """Tag"""

    layout = 'tag'

    def __init__(self, title):
        super(Tag, self).__init__(title=title, slug=title)

    @property
    def posts(self):
        """Get all posts that have this tag"""
        return filter(lambda p: self.title in p._tags, Post.all())


class Category(Tag):
    """Category"""

    layout = 'category'

    @property
    def posts(self):
        """Get all posts that belongs to this category"""
        return filter(lambda p: p._category==self.title, Post.all())
