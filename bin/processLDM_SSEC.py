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
    # To stop data flow to AWIPS, uncomment these lines
    if "GEOW_CONUS" in filepath:
       print "Ignoring Ingest. Removing: {}".format(args.filepath)
       os.remove(filepath)
       raise SystemExit

    # look for "SSEC" in file path to indicate compression is needed even tho ".gz" is missing
    if "SSEC" in filepath:
       # determine the filepath directory and base names
       dirnm = os.path.dirname(filepath)
       basenm = os.path.splitext(filenm)[0]
       # use the directory and base to create a new name with "Alaska" prefix and ".nc" extension
       if "goesr_fog" in basenm:
          # OK, ready to move the file to the ingest directory
          if ".nc" in filepath:
             print "Found GOES17 fog: {}".format(filepath)
             # OK, ready to move the file to the ingest directory
             print "Moving {} to {}".format(filepath, ingestDir)
             try:
                move(filepath,ingestDir)
             except:
                print "Move to ingest failed. Removing: {}".format(filepath)
                os.remove(filepath)
          else:
             print "Removing text or json files: {}".format(filepath)
             os.remove(filepath)
          return
       #
       elif "MIMIC" in basenm:
          print "File MIMIC file: {}/{}".format(dirnm, basenm)
          newfilepath="{}/LDADGRIB_{}".format(dirnm, basenm)
       elif "VIIRS-APRFC" in basenm:
          # The "Alaska_" prefix is needed for "regionalsat" format.
          print "River Ice & Flood product: {}/{}".format(dirnm, basenm)
          newfilepath="{}/Alaska_{}".format(dirnm, basenm)
       else:
          print "Unrecognized SSEC file type: {}".format(filepath)
          os.remove(filepath)
          return
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
       # OK, ready to move the file to the ingest directory
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
