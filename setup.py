#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
]

setup_requirements = [
    # TODO put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

desc = "Color Cone Algorithm with python & opencv"

setup(
    name='color-cone',
    version=__version__,
    description=desc,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Alan Rocha, Diego Aragón and Steve Albo",
    author_email='alan.rocha@udem.edu, diego.aragon@udem.edu and guillermo.albo@udem.edu ',
    url=',
    packages=find_packages(),
)
