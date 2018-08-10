# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='acid',
    version='0.0.0',
    url='https://github.com/codilime/acid',
    author='CodiLime',
    description='CI dashboard for zuul',
    packages=find_packages(exclude=('docs',)),
)

