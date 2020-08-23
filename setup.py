#!/usr/bin/env python

from distutils.core import setup
import setuptools

setup(name='TvTempReport',
      version='0.0.1',
      description='Report child temperatures to Tri-Valley.',
      author='Andrew Baumann',
      author_email='andrew.m.baumann@gmail.com',
      url='none',
      packages=['tv_temp_report'],
      test_requires = [
          "black==19.*",
          "pytest-mockito==0.*",
          "pytest-cov==2.*"
      ],
      install_requires = [
          "selenium==3.*",
          "wheel==0.*",
          "setuptools==49.*",
      ]
     )