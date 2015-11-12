#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Context for template rendering"""

from functools import partial
from datetime import datetime
from peanut.utils import urljoin, real_url


# Filters

def asset(config, value):
    """Get asset file url"""
    asset_path = config.path['asset']
    rel = urljoin(asset_path, value)
    return real_url(config.site.url, rel)

def strftime(value, date_format):
    """Date formatter"""
    return datetime.strftime(value, date_format)

def abs_url(config, value):
    """Absolute url"""
    return urljoin(config.site['url'], value)

def get_filters(config):
    """Get all filters
    """
    return {
        'asset': partial(asset, config),
        'strftime': strftime,
        'abs_url': partial(abs_url, config),
    }
