#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Config unittest
"""

from __future__ import unicode_literals

import os
import unittest
from peanut.config import Config


def config_path():
    curr_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(curr_path, '../example/config.yml')


class TestConfig(unittest.TestCase):
    def test_load(self):
        config = Config(config_path())
        self.assertEqual(config.title, "Peanut Demo")
        self.assertEqual(config.path['draft'], 'drafts')
