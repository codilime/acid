# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='tungsten-ci-acid',
    version='0.0.0',
    url='https://github.com/tungstenfabric/tungsten-ci-acid',
    author='Tungsten Fabric',
    description='CI acid for tungsten fabric repo',
    packages=find_packages(exclude=('docs',)),
)

