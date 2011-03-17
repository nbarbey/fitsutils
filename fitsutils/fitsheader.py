#!/usr/bin/env python
"""
Perform tasks on fits headers from the command line.

cat : Print fits header to standard output.
update : Modify a record value.

Depends on the pyfits package.

Author: Nicolas Barbey
"""
import pyfits
import sys, getopt

LINE_WIDTH = 75
KEY_WIDTH = 8

def print_header(filename, ext=None, rec=None):
    """
    Print header to standard output.

    Arguments
    ---------
    fits : string
      The filename of a fits file.
    ext : optional int (default: None)
      The extension number. If not given, print all extensions.
    rec: optional string (default: None)
      Record names to look up. If not given, print all records.

    Returns
    -------
    Nothing. Prints header to standard output.
    """
    # load file
    try:
        fits = pyfits.fitsopen(filename)
    except(IOError):
        print("File " + filename + " not a fits file or does not exist.")
        return
    # check extension
    n_ext = len(fits)
    if len(ext) == 0:
        ext = xrange(n_ext)
    # print headers
    for e in ext:
        if isinstance(ext, xrange) and not n_ext==1:
            print("-" * LINE_WIDTH)
            print("Extension number " + str(e))
            print("-" * LINE_WIDTH)
        # check records
        replace_rec = False
        if len(rec) == 0:
            crec = fits[e].header.keys()
        else:
            crec = rec
        for r in crec:
            print(r + " " * (KEY_WIDTH - len(r)) +'\t' + str(fits[e].header[r]))

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hnr:e:", ["help", "names", "rec=", "ext="])
    except(getopt.GetoptError, err):
        print(err)
        usage()
        sys.exit(2)
    filenames = args
    ext = list()
    rec = list()
    show_names = False
    if len(args) == 0:
        usage()
        return
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--ext"):
            ext.append(int(a))
        elif o in ("-r", "--rec"):
            rec.append(a)
        elif o in ("-n", "--names"):
            show_names = True
        else:
            assert False, "unhandled option"
    # parse files
    for filename in filenames:
        if show_names:
            print("=" * LINE_WIDTH)
            print("File " + filename)
            print("=" * LINE_WIDTH)
        print_header(filename, ext, rec)
        if show_names:
            print(" ")

def usage():
    print(__usage__)

__usage__ = """Usage: fitsheader [options] [filename(s)]

Options:
  -h, --help        Show this help message and exit
  -e, --ext         Extension number to print.
  -r, --rec         Record string to print.
  -n, --names       Display filenames before headers.
"""

# to call from command line
if __name__ == "__main__":
    main()
