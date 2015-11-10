# -*- coding: utf-8 -*-
"""A static blog generator
"""

from __future__ import print_function

import os
from setuptools import setup

import peanut


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='peanut',
    version=peanut.version,
    license='MIT',
    url = "https://github.com/zqqf16/peanut",
    description='A static blog generator',
    long_description=read('README.md'),
    keywords = "static blog generator",

    author='zqqf16',
    author_email='zqqf16@gmail.com',

    packages=['peanut'],
    include_package_data = True,
    package_data={
        'peanut': [
            'config.yml',
            'themes/default/*.html',
            'themes/default/*.xml',
            'themes/default/assets/css/*.css',
            'themes/default/assets/js/*.js',
        ],
    },

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    install_requires=['Jinja2', 'Markdown', 'Pygments', 'PyYAML', 'six', 'docopt'],

    py_modules=['peanut'],

    entry_points={
        'console_scripts': [
            'peanut=peanut.cmd:main',
        ],
    },
)
