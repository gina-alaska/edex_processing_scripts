#!/usr/bin/env /awips2/python/bin/python
#####################################################################
#
# ncImageQC.py - script for scanning a regionalsat netcdf image file
# for valid (non-zero) pixels and image contrast. If command line 
# input thresholds are not met the script will return "FAIL" 
# Arguments: -c #####   defines a minimum number of valid pixels in
#                       order for the image to pass
#            -r #####   defines the range of pixel values that would
#                       be considered valid for an image to pass
#
#####################################################################
import os, sys
import numpy
import argparse
import Scientific.IO.NetCDF
from Scientific.IO import NetCDF

#####################################################################

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--mincnt', type=int, default=0, action='store', help='min num valid pixels'
    )
    parser.add_argument(
        '-r', '--minrng', type=int, default=0, action='store', help='min range of pixels'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )
    parser.add_argument(
        'filepath', help='netCDF file path'
    )
    args = parser.parse_args()
    return args


def main():
   """ counts valid pixels in satellite netcdf file."""
   #
   pixmax = 0
   pixmin = 0
   pixrng = 0

   args = _process_command_line()
   if args.mincnt == 0 and args.minrng == 0:
      if args.verbose == False:
         print "No thresholds specified...reporting results only"
         args.verbose = True
   #
   if not os.path.exists(args.filepath):
      print "File not found: ",args.filepath 
      raise SystemExit
   try:
      cdf_fh = NetCDF.NetCDFFile(args.filepath, "r")
   except IOError:
       print 'Error opening {}'.format(args.filepath)
       raise SystemExit
   except OSError:
       print 'Error accessing {}'.format(args.filepath)
       raise SystemExit

   varid = cdf_fh.variables['image']
   pixdata = varid.getValue()
   cdf_fh.close()
   #
   pixcnt = numpy.sum(pixdata != 0)
   if pixcnt > 0:
      pixmax = numpy.max(pixdata)
      pixmin = numpy.min(pixdata[numpy.nonzero(pixdata)])
      pixrng = int(pixmax) - int(pixmin)
      
   #
   if args.verbose:
      print "pixmax = {} pixmin = {}".format(pixmax, pixmin)
      print "{} pixels with range: {}".format(pixcnt, pixrng)
   #
   if args.mincnt > 0 and pixcnt < args.mincnt:
      print "FAIL - too few valid pixels"
   elif args.minrng > 0 and pixrng < args.minrng:
      print "FAIL - range too narrow"
   else:
      if args.mincnt == 0 and args.minrng == 0:
         raise SystemExit
      print "PASS"

   return

if __name__ == '__main__':
    # This is only executed if the script is run from the command line.
    main()
