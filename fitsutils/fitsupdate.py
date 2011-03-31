#!/usr/bin/env python
"""
Update fits headers in the command line.

Depends on the pyfits package.

Author: Nicolas Barbey
"""
import pyfits
import sys, getopt

LINE_WIDTH = 75
KEY_WIDTH = 8

def update_header(filename, ext, rec, val):
    """
    Update value in an fits header
    """
    fits = pyfits.fitsopen(filename, "update")
    for e in ext:
        for r, v in zip(rec, val):
            fits[e].header.update(r, v)
    fits.flush()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:r:e:", ["help", "val=", "rec=", "ext="])
    except(getopt.GetoptError, err):
        print(err)
        usage()
        sys.exit(2)
    filenames = args
    ext = list()
    rec = list()
    val = list()
    if len(args) == 0:
        usage()
        return
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--ext"):
            ext.append(a)
        elif o in ("-r", "--rec"):
            rec.append(a)
        elif o in ("-v", "--val"):
            val.append(a)
        else:
            assert False, "unhandled option"
    # update file
    for filename in filenames:
        update_header(filename, ext, rec, val)

def usage():
    print(__usage__)

__usage__ = """Usage: fitsupdate [options] [filename(s)]

Update a fits file header keyword.

Options:
  -h, --help        Show this help message and exit
  -e, --ext         Extension number to update.
  -r, --rec         Record string to update.
  -v, --val         Update record value with val option.
"""

# to call from command line
if __name__ == "__main__":
    main()
