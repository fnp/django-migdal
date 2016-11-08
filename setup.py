#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os.path
from setuptools import setup, find_packages


def whole_trees(package_dir, paths):
    def whole_tree(prefix, path):
        files = []
        for f in (f for f in os.listdir(os.path.join(prefix, path)) if f[0] != '.'):
            new_path = os.path.join(path, f)
            if os.path.isdir(os.path.join(prefix, new_path)):
                files.extend(whole_tree(prefix, new_path))
            else:
                files.append(new_path)
        return files
    prefix = os.path.join(os.path.dirname(__file__), package_dir)
    files = []
    for path in paths:
        files.extend(whole_tree(prefix, path))
    return files

setup(
    name='django-migdal',
    version='0.5',
    author='Radek Czajka',
    author_email='radoslaw.czajka@nowoczesnapolska.org.pl',
    url='',
    packages=find_packages(),
    package_data={'migdal': whole_trees('migdal', ['templates', 'locale'])},
    license='LICENSE',
    description='.',
    long_description="",
)
