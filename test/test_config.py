#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Config unittest
"""

from __future__ import unicode_literals

import os
import unittest
from peanut.config import default_config


class TestConfig(unittest.TestCase):
    def test_load(self):
        config = default_config()
        config.load('config.yml')
        self.assertEqual(config.site['title'], "Peanut Demo")
        self.assertEqual(config.path['draft'], 'drafts')
