#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='resticpy',
    version='0.1.0',
    description='Restic backup Python wrapper',
    author='Michael Lynch',
    author_email='michael@mtlynch.io',
    license="MIT",
    keywords="backup",
    url='https://github.com/mtlynch/resticpy.git',
    packages=['restic'],
    install_requires=[],
    python_requires='>=3.7',
)
