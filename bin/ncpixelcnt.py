#!/usr/bin/env /awips2/python/bin/python

import os, sys
import numpy
import Scientific.IO.NetCDF
from Scientific.IO import NetCDF

def main():
   """ counts valid pixels in satellite netcdf file."""
   if (len(sys.argv) <= 1):
      print "No file path! Syntax: ",sys.argv[0]," {file path}"
      raise SystemExit
   else:
      filepath = sys.argv[1]
   #
   if not os.path.exists(filepath):
      print "File not found: ",filepath 
      raise SystemExit
   try:
      cdf_fh = NetCDF.NetCDFFile(filepath, "r")
   except IOError:
       print 'Error opening {}'.format(args.filepath)
       raise SystemExit
   except OSError:
       print 'Error accessing {}'.format(args.filepath)
       raise SystemExit

   varid = cdf_fh.variables['image']

   pixdata = varid.getValue()
   #
   pixcnt = numpy.sum(pixdata != 0)
   print "{} pixels".format(pixcnt)
   #
   cdf_fh.close()
   return

if __name__ == '__main__':
    # This is only executed if the script is run from the command line.
    main()
