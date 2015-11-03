#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def walk_directory(path, abs_path=True):
    '''Generate directory tree

    @param path: the directory to be walked
    @param abs_path: return absolute file path or not
    
    @return: dictionary, doesn't include the files start with '.'
    '''

    tree = {'dirs':{}, 'files':[]}

    for f in os.listdir(path):
        if f.startswith('.'):
            continue

        p = os.path.join(path, f)
        if os.path.isdir(p):
            d = walk_directory(os.path.join(p))
            tree['dirs'][p] = d

        if os.path.isfile(p):
            tree['files'].append(p)

    return tree
