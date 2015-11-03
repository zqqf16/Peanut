#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Config unittest
"""

from __future__ import unicode_literals

import os
import unittest
from peanut.config import load, config


class TestConfig(unittest.TestCase):
    def test_load(self):
        load('config.yml')
        self.assertEqual(config.site['title'], "Peanut Demo")
        self.assertEqual(config.path['draft'], 'drafts')
