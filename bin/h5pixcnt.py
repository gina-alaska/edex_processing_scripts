#!/usr/bin/env /awips2/python/bin/python

import os, sys
import numpy
import h5py

def main():
   """ counts valid pixels in satellite netcdf file."""
   if (len(sys.argv) <= 1):
      print ("No file path! Syntax: ",sys.argv[0]," {file path}")
      raise SystemExit
   else:
      filepath = sys.argv[1]
   #
   if not os.path.exists(filepath):
      print ('File not found: {}'.format(filepath))
      raise SystemExit
   try:
      #cdf_fh = NetCDF.NetCDFFile(filepath, "r")
      h5_fh = h5py.File(filepath, "r")
   except IOError:
      print ('Error opening: {}'.format(filepath))
      raise SystemExit
   except OSError:
      print ('Error accessing: {}'.format(filepath))
      raise SystemExit

   dvar = h5_fh.get('data')
   dnp = numpy.array(dvar)
   pixcnt = numpy.sum(dnp != 0)
   print ("{} pixels".format(pixcnt))
   #
   h5_fh.close()
   return

if __name__ == '__main__':
    # This is only executed if the script is run from the command line.
    main()
