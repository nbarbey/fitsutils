==============================
fitsutils
==============================

What is fitsutils ?
===================

This is a small set of scripts to easily handle Flexible Image
Transport System (FITS) files in the command-line. It contains:

- fitsheader: Display the header of a FITS file to stdout.

- fitsfilter: Filter a list of files using conditions on header content.

- fitsview: Display a simple FITS image (requires matplotlib).

- fitsarray: A module to load FITS data as ndarray storing header as
  an attribue.



Requirements
=============

You will need pyfits, numpy and matplotlib.


Installation
============

Get the source code, e.g:

..raw: git clone https://github.com/nbarbey/fitsutils

Install with distutils from new directory:

..raw: python setup.py install

If you do not have root privilege, you can install in your home:

..raw: python setup.py install --prefix=$HOME/local/
