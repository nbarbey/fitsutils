#!/usr/bin/env python
import getopt
import sys
import pyfits

__all__ = ["fitsfilter", "add_quotes_to_str", "add_quotes_to_keys"]

def fitsfilter(filenames, test_str, ext=0):
    """
    Filter a list of fits filenames checking a test string.

    Arguments:
    ----------
    filenames: (list of strings)
    list of string corresponding to fits filenames.

    test_str: (string)
    a test string of the form :

    (a[NAXIS] == 3 and a[NAXIS1] == 1024) or a[NAXIS2] == 2

    Returns:
    --------
    out_files: (list of strings)
    list of string corresponding to fits filenames verifying the test.

    Notes:
    ------
    The use of 
    """
    out_files = list()
    # parse filenames
    for f in filenames:
        test = True
        try:
            a = pyfits.fitsopen(f)[ext].header
        # file does not exist
        except IOError:
            test = False
        # extension does not exist
        except IndexError:
            test = False
        if "a" in locals():
            try:
                test_str = add_quotes_to_str(test_str)
                test_str = add_quotes_to_keys(test_str)
                exec_str = " ".join(("if", "not", "(" + test_str + "):", "test = False"))
                exec(exec_str)
            # one of the key does not exist
            except KeyError:
                test = False
            if test:
                out_files.append(f)
    return out_files

def add_quotes_to_keys(s):
    import re
    # match any string key
    c = re.compile(r"[[A-Z]+[0_9]*]")
    g = re.findall(c, s)
    for gi in g:
        gt = gi.replace("[", "[\"")
        gt = gt.replace("]", "\"]")
        s = s.replace(gi, gt)
    return s

def add_quotes_to_str(s):
    import re
    # split with spaces
    sl = s.split(" ")
    sl2 = list()
    for si in sl:
        # test if the first character is a letter
        if si[0].isalpha() and not ("[" in si or "]" in si or si == "and" or si == "or" or si == "in"):
            sl2.append("\"" + si + "\"")
        else:
            sl2.append(si)
    return " ".join(sl2)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:e:", ["help", "test=", "ext="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    test_str = ""
    ext = 0
    verbose = False
    if len(args) == 0:
        usage()
        return
    for o, a in opts:
        if o in ("-t", "--test"):
            test_str = a
        elif o in ("-e", "--ext"):
            ext = int(a)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    # filter files
    out = fitsfilter(args, test_str, ext)
    if out is not None:
        for o in out:
            print o

def usage():
    print(__usage__)

__usage__ = """Usage: fitsfilter [options] [filename(s)]

Options:
  -h, --help        Show this help message and exit
  -t, --test        Defines a test to perform on a fits header record.
                    If no test is given, outputs filename(s).
  -e, --ext         Extension where the record should be looked for.
"""

# to call from command line
if __name__ == "__main__":
    main()
