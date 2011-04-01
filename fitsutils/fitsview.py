#!/usr/bin/env python
"""
Display fits images using pyfits and matplotlib.

Author: Nicolas Barbey
"""

def show_fits(filename, ext=None, outfile=None):
    # imports
    import matplotlib.pylab as mp
    import pyfits
    # open file
    fits = pyfits.fitsopen(filename)
    if ext is None:
        # display the first image-like extension
        for e in xrange(len(fits)):
            a = fits[e].data
            if a.ndim == 2:
                break
    else:
        a = fits[ext].data
    mp.imshow(a)
    if outfile is None:
        mp.show()
    else:
        mp.savefig(outfile)

def main():
    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:", ["help", "ext="])
    except(getopt.GetoptError, err):
        print(err)
        usage()
        sys.exit(2)
    outfile = None
    if len(args) == 0:
        usage()
        sys.exit(2)
    filename = args[0]
    if len(args) > 1:
        outfile = args[1]
    ext = list()
    if len(args) == 0:
        usage()
        return
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--ext"):
            ext.append(int(a))
        else:
            assert False, "unhandled option"
    # parse files
    if len(ext) == 0:
        ext = list((0,))
    for e in ext:
        show_fits(filename, e, outfile)

def usage():
    print(__usage__)

__usage__ = """Usage: fitsview [options] filename [output]

If no output file is provided, display the image.
Otherwise, save the plot as an image to the output file.

Options:
  -h, --help        Show this help message and exit.
  -e, --ext         Extension number to print.
"""

# to call from command line
if __name__ == "__main__":
    main()
