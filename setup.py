#!/usr/bin/env python
from setuptools import setup

setup(
    name='mercury',
    version='0.4.2',
    author='Rahmanda Wibowo',
    author_email='rahmandawibowo@gmail.com',
    url='https://github.com/rahmanda/mercury-py',
    scripts=['src/mercury-py'],
    packages=['mercury'],
    package_dir={'mercury': 'src/mercury'}
)
