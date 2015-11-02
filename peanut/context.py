#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Context for template rendering"""

from peanut.config import config

__all__ = ['filters']


# Filters

def asset(value):
    """Get asset file url"""
    asset_path = config.path['asset']
    if not asset_path.endswith('/'):
        asset_path += '/'
    return asset_path+value

filters = {
    'asset': asset
}
