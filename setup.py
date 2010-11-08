#!/usr/bin/env python

from distutils.core import setup
import subprocess


# Obtain version information from git
try:
    p = subprocess.Popen(['git', 'describe'], stdout=subprocess.PIPE)
    (pstdout, _) = p.communicate()
    version = pstdout.strip()
except OSError:
    import sys
    print >> sys.stderr, "Please install git to have version information on your build"
    sys.exit(1)


setup(name='bless',
      version=version,
      description='Curses Widget library for python',
      author='Gerard Lledo',
      author_email='gerard.lledo@gmail.com',
      url='https://github.com/gerard/bless',
      packages=['bless', 'bless.widgets'],
      package_dir = {'': 'src'},
      scripts=['apps/list.py'],
     )
