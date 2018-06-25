#!/usr/bin/env python
"""Get all the files in datastore netcdf file."""

import argparse
import os
import datetime
from datetime import datetime
import time

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--day', action='store', help='day of month to search'
    )
    parser.add_argument(
        '-t', '--type', action='store', default='regionalsat', \
        help='type of file (goesr, grib, nucaps, regionalsat)'
    )
    parser.add_argument(
        '-m', '--match', action='store', help='string pattern to match'
    )
    #parser.add_argument(
    #    '-v', '--verbose', action='store_true', help='verbose flag'
    #)
    args = parser.parse_args()
    return args

#####################################################################
def get_filepaths(directory):
    """ generate the filenames in a directory tree by walking down
    the tree. """

    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
           # Join the two strings to form the full path
           filepath = os.path.join(root,filename)
           file_paths.append(filepath)

    return file_paths

#####################################################################

def main():
    """Call to run script."""
    basedirectory = "/data_store/manual"

    args = _process_command_line()
    searchpath = "{}/{}".format(basedirectory,args.type)

    curtime  = datetime.utcnow()
    if args.day is not None:
        subDir = '{}{:02}'.format(curtime.strftime("%Y%m"),int(args.day))
        print subDir
        paths = get_filepaths('{}/{}'.format(searchpath,subDir))
    else:
        subDir = curtime.strftime("%Y%m%d")
     
    paths = get_filepaths('{}/{}'.format(searchpath,subDir))
    paths.sort(reverse=True)

    #if args.match:
    #   print "Matching {}".format(args.match)
    #
    count = 0
    for path in paths:
       if args.match:
          if args.match in path:
             print path
             count += 1
       else:
          print path
          count += 1

    if count > 0:
       print "Products found: {}".format(count)
    else:
       print "Nothing matches criteria."
    return

if __name__ == '__main__':
    main()
