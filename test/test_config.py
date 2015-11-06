#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Config unittest
"""

import os
import unittest

from peanut.options import configs, load_configs

PWD = os.path.abspath(os.path.dirname(__file__))

class TestConfig(unittest.TestCase):
    def test_load(self):
        configs.pwd = os.path.join(PWD, 'test_site')
        load_configs('config.yml')
        self.assertEqual(configs.site['title'], "Peanut Demo")
        self.assertEqual(configs.path['draft'], 'drafts')
