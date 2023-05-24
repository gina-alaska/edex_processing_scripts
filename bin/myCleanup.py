#!/usr/bin/env /awips2/python/bin/python

import os, sys
import argparse
import datetime
from time import strftime
from datetime import datetime, timedelta

#####################################################################

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )
    parser.add_argument(
        'dirpath', help='directory to keep clean'
    )
    parser.add_argument(
        '-dh', '--deltahrs', type=int, action='store', default=3,
        help='time delta in hrs')
    args = parser.parse_args()
    return args

#####################################################################

def main():
   """ counts valid pixels in satellite netcdf file."""
   args = _process_command_line()

   # make sure the path name if valid
   if os.path.isdir(args.dirpath):
      backtime = datetime.utcnow() - timedelta(hours=args.deltahrs)
      backsecs = int(backtime.strftime("%s"))
      #timedelay = time.time() - args.deltasecs 
      if args.verbose:
         print ("Checking for gzip files older than {}.".format(
             backtime.strftime("%Y-%m-%d %H:%M:%S")))
      cnt = 0
      for filename in os.listdir(args.dirpath):
         filepath = os.path.join(args.dirpath,filename)
         mtime=os.path.getmtime(filepath)
         if args.verbose:
            print ("{} {}".format(datetime.fromtimestamp(mtime),filepath))
         if mtime < backsecs:
            print ("OLD: {}".format(filepath))
            if ".gz" in filepath:
               #pass
               print ("Removing: {}".format(filepath))
               os.unlink(filepath) # uncomment only if you are sure
               cnt += 1
            else:
               print ("No delete. Missing gz extension: {}".format(filename))
                
   else:
       print ("Invalid path: {}".format(args.dirpath))

   if args.verbose:
      print ("Files removed: {}".format(cnt))

   return

if __name__ == '__main__':
    # This is only executed if the script is run from the command line.
    main()
