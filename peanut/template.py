#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Template"""

import jinja2

from jinja2 import ChoiceLoader, FileSystemLoader, PackageLoader


loader = jinja2.ChoiceLoader([
    FileSystemLoader('/path/to/local/template'),
    PackageLoader('peanut', 'themes/default')
])
