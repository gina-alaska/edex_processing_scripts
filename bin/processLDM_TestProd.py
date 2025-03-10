#!/usr/bin/env /awips2/python/bin/python
"""Get all the files in datastore netcdf file."""

import argparse
import os, sys
import gzip
from shutil import copy, move
import datetime
from datetime import datetime, timedelta
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

    ingestDir = "/data_store/dropbox"

    args = _process_command_line()

    ###################################
    # clean up logs...remove an old log that is a fixed number of days old (if still present)
    backdays = 5
    backtime = curtime - timedelta(days=backdays)
    oldlogpath="/opt/ldm/var/logs/edex-ingest-LDMsat-{}.log".format(backtime.strftime("%Y%m%d"))
    if os.path.isfile(oldlogpath): 
       os.remove(oldlogpath) 
    ###################################

    print ("------\n{}Z {}\nReceived: {}".format(curtime.strftime("%Y%m%d %H%M"), sys.argv[0], args.filepath))

    if not os.path.exists(args.filepath):
        print ("File not found: {}".format(args.filepath))
        raise SystemExit

    filepath = args.filepath
    #print ("Valid filepath: {}".format(filepath))

    ################################################3
    # To stop data flow to AWIPS, uncomment these lines 
    #os.remove(filepath)
    #raise SystemExit
    ################################################3
    #
    # this section is only for support of remote file downloads (i.e. carl)
    #if not os.path.exists(queueDir):
    #   os.makedirs(queueDir)
    #print ("copying {} to {}".format(filepath, queueDir))
    #copy(filepath,queueDir)

    # look for ".gz" in file path to indicate compression is needed
    if "TEST_UAF" in filepath:
       # determine the filepath directory and base names
       dirnm = os.path.dirname(filepath)
       filenm = os.path.basename(filepath)
       basenm = os.path.splitext(filenm)[0]
       newfilenm = filenm[5:]
       print ("New filename: {}".format(newfilenm))
       # use the directory and base to create a new name without the "TEST" prefix
       ingestPath="{}/{}".format(ingestDir, newfilenm)
       #
       # Now the file is uncompressed and renamed with the "Alaska_" prefix. 
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
       # 
       ##############################################
       #
       # OK, ready to move the file to the ingest directory
       print ("Moving {} to {}".format(filepath, ingestPath))
       try:
          move(filepath,ingestPath)
       except:
          print ("Move to ingest failed. Removing: {}".format(filepath))
          os.remove(filepath)
       #
    # a file with a UAF prefix and no ".gz" extension is unknown
    else:
       print ("Unrecognized file format: {}".format(filepath))
    #
    return

if __name__ == '__main__':
       # Now the file is uncompressed and renamed with the "Alaska_" prefix.
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
    main()
