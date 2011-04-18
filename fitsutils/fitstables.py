"""
To read and write binary tables.

Contains:

 - mrdfits
 - mwrfits

"""
import os
import numpy as np
import pyfits

def mrdfits(filename, extension=1, transpose=False, verbose=False):
    """
    Read a an extended fits file.
    Try to emulate mrdfits.pro

    Arguments
    ---------
    filename: string
    extension: int
    transpose: bool
    verbose: bool

    Returns
    -------
    A dictionary of arrays

    """
    if verbose:
        print 'extension = ', extension
    # load data
    fits = pyfits.fitsopen(filename)
    hdu = fits[extension]
    data = hdu.data
    if not (isinstance(hdu, pyfits.BinTableHDU)
            or isinstance(hdu, pyfits.TableHDU)):
        # this is an "image"
        return data
    # else this is a table (ASCII or Binary)
    header = hdu.header
    #  create dictionnary
    mydict = dict.fromkeys(data._names)
    # beware order is not kept
    # fill the dictionnary
    for i, name in enumerate(data._names):
       mydim = "tdim{0}".format(i+1)
       if header.has_key(mydim):
           myshape = header[mydim]
           # n = [int(i) for i in header.strip('()').split(',')]
           exec('myshape = ' + header[mydim])
           # need to reverse shape due to FITS convention
           # (quick axis first in FITS and last in Python)
           myshape = myshape[::-1]
           mydict[name] = data.field(name).reshape(myshape)
           if transpose:
               mydict[name] = mydict[name].transpose()
       else:
           mydict[name] = data.field(name).ravel()
    #
    # check
    if verbose:
        for k, v in mydict.iteritems():
            print k, v[0:1]
    #
    return mydict

def mwrfits(mydict, filename, clobber=False, ascii=False):
    """
    Write an dictionary as a binary table in a FITS file.

    Shape order is reverted to satisfy the FITS conventions
    (quick axis is first in FITS and second in python)

    Arguments
    ---------
    mydict: dict of ndarrays
    filename: string
      The name of the written fits file.
    clobber: bool
       Overwrites the output file if True.

    Returns
    --------
    Returns nothing.
    
    Exceptions
    ---------
    ValueError if mydict is not a dict of arrays
    """
    # check that dict contains only arrays
    for k, v in mydict.iteritems():
        if not isinstance(v, np.ndarray):
            raise ValueError("Expected a dict of arrays.")

    # convert dict of ndarray as an array of size 1
    mydtype = list()
    for k, v in mydict.iteritems():
        mydtype.append((k, str(v.shape) + v.dtype.str))
    arr = np.zeros(1, dtype=mydtype)
    for k, v in mydict.iteritems():
        arr[k] = v
    if ascii:
        raise NotImplemented() # hdu = pyfits.TableHDU(arr) # not working !
    else:
        hdu = pyfits.BinTableHDU(arr)
    # shape order is reverted to satisfy the FITS conventions
    # (quick axis is first in FITS and second in python)
    for i, v in enumerate(mydict.values()):
        hdu.header.update('TDIM' + str(i + 1), str(v.shape[::-1]))
    hdu.writeto(filename, clobber=clobber)
