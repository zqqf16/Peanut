#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Object pool
"""

import inspect


class ObjectPool(type):
    """Meta class to implement a simple "object pool".
    """

    def __new__(mcs, name, bases, attrs):
        """Add an attribute "_pool" and two classmethods "all" and "get".
        """
        def all(cls):
            """Get all instances from the pool
            """

            return cls._pool.values()

        def get(cls, identity):
            """Get an instance by identity
            """

            return cls._pool.get(identity)

        attrs['_pool'] = {}
        attrs['all'] = classmethod(all)
        attrs['get'] = classmethod(get)

        return super(ObjectPool, mcs).__new__(mcs, name, bases, attrs)


    def __call__(cls, *args, **kwargs):
        """Get instance from pool or create a new one
        """

        id_key = getattr(cls, '_identity', None)
        identity = None

        if id_key:
            call_args = inspect.getcallargs(cls.__init__, None, *args, **kwargs)
            identity = call_args.get(id_key)
        identity = identity or tuple(*args, **kwargs)

        if identity in cls._pool:
            # Get from pool
            return cls._pool[identity]

        # Create a new one
        instance = super(ObjectPool, cls).__call__(*args, **kwargs)
        cls._pool[identity] = instance

        return instance
