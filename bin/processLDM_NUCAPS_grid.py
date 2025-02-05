#!/usr/bin/env python
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

    ingestDir = "/data_store/dropbox"

    args = _process_command_line()

    print "------\n{}Z {}\nReceived: {}".format(curtime.strftime("%Y%m%d %H%M"), sys.argv[0], args.filepath)

    if not os.path.exists(args.filepath):
        print "File not found: {}".format(args.filepath)
        raise SystemExit

    filepath = args.filepath
    #print "Valid filepath: {}".format(filepath)
    #
    ################################################
    # To stop data flow to AWIPS, uncomment these lines
    #os.remove(filepath)
    #raise SystemExit
    ################################################
    #
    # this section is only for support of remote file downloads (i.e. carl)
    #if not os.path.exists(queueDir):
    #   os.makedirs(queueDir)
    #print "copying {} to {}".format(filepath, queueDir)
    #copy(filepath,queueDir)
    #
    # look for ".gz" in file path to indicate compression is needed
    if ".gz" in filepath:
       # determine the new base path minus the ".gz" extension
       newfilepath = os.path.splitext(filepath)[0]
       # use the directory and base to create a new name with the ".grb2" extension
       if ".grb2" not in newfilepath:
          print "Unrecognized file format: {}".format(filepath)
          raise SystemExit
       #
       # open the compressed file and read out all the contents
       inF = gzip.GzipFile(filepath, 'rb')
       s = inF.read()
       inF.close()
       # now write uncompressed result to the new filename
       outF = file(newfilepath, 'wb')
       outF.write(s)
       outF.close()
       #
       # make sure the decompression was successful
       if not os.path.exists(newfilepath):
          print "Decompression failed: {}".format(filepath)
          raise SystemExit
       #
       print "File decompressed: {}".format(newfilepath)
       # redirected compression copies to a new file so old compressed file needs to be removed
       os.remove(filepath)
       # set the filepath to point to the uncompresses name
       filepath = newfilepath
       #
       # Now the file is uncompressed  with the ".grb2" suffix.
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
       # 
       ##############################################
       #
       # OK, ready to move the file to the ingest directory
       #
       print "Moving {} to {}".format(filepath, ingestDir)
       try:
          move(filepath,ingestDir)
       except:
          print "Move to ingest failed. Removing: {}".format(filepath)
          os.remove(filepath)
       #
    # a file with a UAF prefix and no ".gz" extension is unknown
    else:
       print "Unrecognized file format: {}".format(filepath)
    #
    return

if __name__ == '__main__':
    main()
