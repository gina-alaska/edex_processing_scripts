#!/usr/bin/env /awips2/python/bin/python
"""Get all the files in datastore netcdf file."""

import argparse
import os, sys
import glob
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

    ingestDir = "/awips2/edex/data/manual"
    workingDir = "/data_store/download"

    args = _process_command_line()

    ###################################
    # clean up logs...remove an old log that is a fixed number of days old (if still present)
    backdays = 5
    backtime = curtime - timedelta(days=backdays)
    oldlogpath="/opt/ldm/var/logs/edex-ingest-LDMsat-{}.log".format(backtime.strftime("%Y%m%d"))
    if os.path.isfile(oldlogpath): 
       os.remove(oldlogpath) 
    ###################################

    print "------\n{}Z {}\nReceived: {}".format(curtime.strftime("%Y%m%d %H%M"), sys.argv[0], args.filepath)

    if not os.path.exists(args.filepath):
        print "File not found: {}".format(args.filepath)
        raise SystemExit
    processFlag = 1
    filepath = args.filepath
    #print "Valid filepath: {}".format(filepath)

    # look for ".gz" in file path to indicate compression is needed
    if "OR_ABI" in filepath:
       # determine the filepath directory and base names
       os.chdir(workingDir)
       dirnm = os.path.dirname(filepath)
       filenm = os.path.basename(filepath)
       basenm = os.path.splitext(filenm)[0]
       #if processFlag:
       if "G17" in filepath:
         
          bgntime  = datetime.utcnow()
          print "Converting {} to Level 2".format(filepath)
          print "Start time: {}Z".format(bgntime.strftime("%Y%m%d %H%M"))
          #commandstr = "/home/awips/axi-tools/bin/cmi_changer.sh -E OT -R ECONUS -S CONUS {}".format(filepath)
          commandstr = "/home/awips/axi-tools/bin/cmi_changer.sh -E OT -R WCONUS -S CONUS {}".format(filepath)
          os.system(commandstr)
          #
          # OK, ready to move the file to the ingest directory
          convertFlag = 0
          for thisfile in glob.glob('./OT_WCONUS*'):
             # OK, ready to move the file to the ingest directory
             print "Moving {} to {}".format(thisfile, ingestDir)
             try:
                move(thisfile,ingestDir)
                convertFlag = 1
             except:
                print "Move to ingest failed. Removing: {}".format(thisfile)
                try:
                   os.remove(thisfile)
                except:
                   print "Unable to remove: {}".format(thisfile)
             #
          if convertFlag:
             endtime  = datetime.utcnow()
             print "Conversion and ingest was successful"
             print "End time: {}Z".format(endtime.strftime("%Y%m%d %H%M"))
          else:
             print "Conversion was unsuccessful"
         
          # now convert to an SCMI grid
          #if "M3C13" in filepath:
          #   print "Creating SCMI tiles"
          #   commandstr = "/home/awips/geo2grid/bin/geo2grid.sh -r abi_l1b -w scmi --sector_id TR04 -f {}".format(filepath) 
          #   os.system(commandstr)
 
       # Make sure to remove Level 1b files 
       print "Removing: {}".format(filepath)
       os.remove(filepath)
       #
    # a file with a UAF prefix and no ".gz" extension is unknown
    else:
       print "Unrecognized file format. Removing: {}".format(filepath)
       os.remove(filepath)
    #
    return

if __name__ == '__main__':
       # Now the file is uncompressed and renamed with the "Alaska_" prefix.
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
    main()
