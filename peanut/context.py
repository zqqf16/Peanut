#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Context for template rendering"""

try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin

from datetime import datetime
from peanut.config import config

__all__ = ['filters']


# Filters

def asset(value):
    """Get asset file url"""
    asset_path = config.path['asset']
    return urljoin(asset_path, value)

def strftime(value, date_format):
    """Date formatter"""
    return datetime.strftime(value, date_format)

def abs_url(value):
    """Absolute url"""
    return urljoin(config.site['url'], value)

filters = {
    'asset': asset,
    'strftime': strftime,
    'abs_url': abs_url,
}
