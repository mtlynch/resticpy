#!/usr/bin/env python

import os.path

import setuptools

setuptools.setup(
    name='resticpy',
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     'README.md')).read(),
    long_description_content_type="text/markdown",
    version='1.0.6',
    description='Restic backup Python wrapper',
    project_urls={
        "repository": "https://github.com/mtlynch/resticpy",
    },
    author='Michael Lynch',
    author_email='michael@mtlynch.io',
    license="MIT",
    keywords="backup",
    url='https://github.com/mtlynch/resticpy.git',
    packages=['restic', 'restic.internal'],
    install_requires=[],
    python_requires='>=3.7',
)
