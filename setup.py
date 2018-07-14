# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='tungsten-ci-dashboard',
    version='0.0.0',
    url='https://github.com/tungstenfabric/tungsten-ci-dashboard',
    author='Tungsten Fabric',
    description='CI dashboard for tungsten fabric repo',
    packages=find_packages(exclude=('docs',)),
)

