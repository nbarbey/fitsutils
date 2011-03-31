#!/usr/bin/env python
from numpy.distutils.core import Extension, setup
from numpy import get_include
from os.path import join
import sys
setup(name='fitsutils',
      version='0.2.0',
      description='A set of small command-line tools for FITS files',
      author='Nicolas Barbey',
      author_email='nicolas.a.barbey@gmail.com',
      requires = ['numpy (>1.3.0)', 'pyfits'],
      packages=['fitsutils'],
      scripts=['fitsutils/fitsheader',
               'fitsutils/fitsfilter',
               'fitsutils/fitsupdate',
               'fitsutils/fitsview'],
      )
