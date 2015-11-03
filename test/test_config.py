#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Config unittest
"""

from __future__ import unicode_literals

import os
import unittest
from peanut.config import load, config


def abs_path(path):
    curr_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.abspath(os.path.join(curr_path, path))


class TestConfig(unittest.TestCase):
    def test_load(self):
        load(abs_path('../example/config.yml'))
        self.assertEqual(config.title, "Peanut Demo")
        self.assertEqual(config.path['draft'], 'drafts')
        self.assertEqual(config.theme_path, abs_path('../peanut/themes/default'))
