#!/usr/bin/env python

from distutils.core import setup

setup(name='bless',
      version='0.1',
      description='Curses Widget library for python',
      author='Gerard Lledo',
      author_email='gerard.lledo@gmail.com',
      url='https://github.com/gerard/bless',
      packages=['bless', 'bless.widgets'],
      package_dir = {'': 'src'},
      scripts=['apps/list.py'],
     )
