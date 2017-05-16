#!/usr/bin/env python
from setuptools import setup

setup(
    name='mercury',
    version='0.4.3',
    author='Rahmanda Wibowo',
    author_email='rahmandawibowo@gmail.com',
    url='https://github.com/rahmanda/mercury-py',
    scripts=['src/mercury'],
    packages=['mercury_py'],
    package_dir={'mercury_py': 'src/mercury_py'}
)
