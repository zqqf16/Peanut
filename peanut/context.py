#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Context for template rendering"""

from datetime import datetime
from peanut.config import config

__all__ = ['filters']


# Filters

def asset(value):
    """Get asset file url"""
    asset_path = config.path['asset']
    if not asset_path.endswith('/'):
        asset_path += '/'
    return asset_path+value

def strftime(value, date_format):
    """Date formatter"""
    return datetime.strftime(value, date_format)

filters = {
    'asset': asset,
    'strftime': strftime,
}
