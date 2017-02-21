#!/usr/bin/env python

from setuptools import setup

setup(name='thesisplots',
      version='0.1',
      description='DRY generation of scientific plots',
      author='Davide Olianas',
      author_email='admin@davideolianas.com',
      url='',
      packages=['thesisplots'],
      entry_points={
          'console_scripts': [
              'thplot = thesisplots.cli:main']
      },
      install_requires=['numpy', 'matplotlib', 'appdirs'],
      tests_require=['pytest', 'pytest-cov'],
      extras_require={
          'dev': [ 'Sphinx' ]
      }
     )