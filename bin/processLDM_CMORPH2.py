#!/usr/bin/env /awips2/python/bin/python
"""Get all the files in datastore netcdf file."""

import argparse
import os, sys
import gzip
from shutil import copy, move
import datetime
from datetime import datetime
import time

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filepath', help='satellite sensors to download'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )
    args = parser.parse_args()
    return args

#####################################################################

def main():
    """Call to run script."""
    curtime  = datetime.utcnow()
    logpath="/opt/ldm/var/logs/edex-ingest-LDMsat-{}.log".format(curtime.strftime("%Y%m%d"))
    sys.stdout = sys.stderr = open(logpath, 'a+')

    ingestDir = "/awips2/edex/data/manual"
    queueLimit = 60 
    args = _process_command_line()

    print "------\n{}Z {}\nReceived: {}".format(curtime.strftime("%Y%m%d %H%M"), sys.argv[0], args.filepath)
    #
    if not os.path.exists(args.filepath):
        print "File not found: {}".format(args.filepath)
        raise SystemExit
    #
    filepath = args.filepath
    filenm = os.path.basename(filepath)
    #print "Valid filepath: {}".format(curtime.strftime("%Y%m"),args.day, filepath)
    #
    ################################################
    statFlag = 0
    if "CMORPH2" in filepath:
       # determine the filepath directory and base names
       dirnm = os.path.dirname(filepath)
       basenm = os.path.splitext(filenm)[0]
       # move the file to manual ingest
       try:
          move(filepath,ingestDir)
          statFlag = 1
       except:
         print "Move to ingest failed. Removing: {}".format(filepath)
    # Unknown file format
    else:
       print "Unrecognized file format Removing: {}".format(filepath)
    if statFlag == 0:
       try:
          os.remove(filepath)
       except:
         print "Unable to remove: {}".format(filepath)
    #
    return

if __name__ == '__main__':
    main()
