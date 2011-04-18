#!/usr/bin/env python

"""
Unit tests
"""
import nose
import os
import numpy as np
from fitsutils import fitstables

# test data
location = "http://www.cv.nrao.edu/fits/data/samples/bintable/"
filename = "testdata.fits"

# data to check against test file
keys = ['FE361', 'MG368', 'FE335', 'HE304', 'DEL_TIME']
shapes = ((120, 120, 10),
          (120, 120, 10),
          (120, 120, 10),
          (120, 120, 10),
          (120,),)

# test data for writing
test_dict = {'x':np.arange(6),
             'y':np.ones(6)}

outfile = "test_fitstables.fits"

# utility functions

def assert_dict_almost_equal(dict1, dict2, decimal=6, verbose=False):
    """
    Compares dictionaries of array and test if arrays are almost equals.
    Stops at the first difference.
    If values are not dictionnaries, strict equality is tested.

    Arguments
    ---------
    dict1, dict2 : dictionaries
    decimal: int
      To which decimal arrays should be equals.
    verbose: bool
      Print information about dict differences if True

    Returns
    --------
    out: bool
      True if dict1 and dict2 are almost equals.
    """
    # test dict have same keys
    if not len(set(dict1) - set(dict2)) == 0:
        if verbose:
            print("dict1 and dict2 do not have the same keys.")
        return False
    # now test for arrays equality
    for k, v1, v2 in zip(dict1.keys(), dict1.values(), dict2.values()):
        try:
            np.testing.assert_array_almost_equal(v1, v2, decimal=decimal,
                                                 verbose=verbose)
        except AssertionError:
            if verbose:
                print("Array %s differs in dict1 and dict2." % k)
            return False
        except TypeError:
            # if not recognize by assert_array_almost_equal test strict equality
            if np.any(v1 != v2):
                if verbose:
                    print("Values %s differs in dict1 and dict2" % k)
                return False
            #endif
    # good
    return True

def testdata_exists():
    """
    Returns True if test filename is found
    """
    return os.path.exists(filename)

def get_testdata():
    if not testdata_exists():
        os.system("wget " + location + filename)

def outdata_exists():
    return os.path.exists(outfile)

# test reading data
def test_mrdfits():
    """
    Test that file is readable by mrdfits
    """
    t = fitstables.mrdfits(filename)

def test_keys():
    t = fitstables.mrdfits(filename)
    assert t.keys() == keys

def test_shapes():
    t = fitstables.mrdfits(filename)
    for i, v in enumerate(t.values()):
        assert v.shape == shapes[i]

# test writing data
def test_mwrfits():
    fitstables.mwrfits(test_dict, outfile, clobber=True)

def test_write_read():
    fitstables.mwrfits(test_dict, outfile, clobber=True)
    dict2 = fitstables.mrdfits(outfile)
    assert_dict_almost_equal(test_dict, dict2)

if __name__ == "__main__":
    nose.run(argv=['', __file__])
