==============================
fitsutils
==============================

What is fitsutils ?
===================

This is a small set of scripts to easily handle Flexible Image
Transport System (FITS) files in the command-line. It contains:

- fitsheader: Display the header of a FITS file to stdout.

- fitsupdate: Update the header of a FITS file.

- fitsfilter: Filter a list of files using conditions on header content.

- fitsview: Display a simple FITS image (requires matplotlib).

- fitsarray: A module to load FITS data as ndarray storing header as
  an attribue.

- fitstables: A module to load and write FITS binary tables as
  dictionaries of ndarrays.

Requirements
=============

You will need pyfits and numpy (and matplotlib for fitsview).

Installation
============

Get the source code, e.g::

  git clone https://github.com/nbarbey/fitsutils

Install with distutils from new directory::

  python setup.py install

If you do not have root privilege, you can install in your home::

  python setup.py install --prefix=$HOME/local/
