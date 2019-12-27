#!/usr/bin/env python

import setuptools

setuptools.setup(name='pyrestic',
      version='0.1a1.dev002',
      description='Restic backup Python wrapper',
      author='JunWang',
      author_email='jstzwj@aliyun.com',
      license="MIT",
      keywords="backup",
      url='https://github.com/jstzwj/PyRestic.git',
      packages=[
            'restic',
            'restic.test'
      ],
      install_requires=[
      ],
      python_requires='>=3.7',
     )