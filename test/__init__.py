#!/usr/bin/env python

import os

def abs_path(path):
    curr_path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.abspath(os.path.join(curr_path, path))

os.chdir(abs_path('test_site'))
