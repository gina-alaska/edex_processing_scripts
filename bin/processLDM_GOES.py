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

    ingestDir = "/data_store/dropbox"
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

    # look GOES prefix in file path
    if "OR_ABI" in filepath:
       # determine the filepath directory and base names
       os.chdir(workingDir)
       dirnm = os.path.dirname(filepath)
       filenm = os.path.basename(filepath)
       basenm = os.path.splitext(filenm)[0]
       #Only process GOES-17
       if "G17" in filepath and "RadF" in filepath:
          channel = basenm[16:21]
          bgntime  = datetime.utcnow()
          print "Converting {} to Level 2: {}".format(channel, filepath)
          print "Start time: {}Z".format(bgntime.strftime("%Y%m%d %H%M"))
          #commandstr = "/home/awips/axi-tools/bin/cmi_changer.sh -E OT -R ECONUS -S CONUS {}".format(filepath)
          commandstr = "/home/awips/axi-tools/bin/cmi_changer.sh -E OT -R WCONUS -S CONUS {}".format(filepath)
          try:
             os.system(commandstr)
          except:
             print "Conversion was unsuccessful"
          #
          # OK, ready to move the file to the ingest directory
          for thisfile in glob.glob('./OT_WCONUS*'):
             if not channel in thisfile:
                 #print "No {} in {}".format(channel, thisfile)
                 continue
             #if not os.path.exists(thisfile):
             #   print "File does not exist: {}".format(thisfile)
             #   continue
             # OK, ready to instert the converted file to LDM
             thisfilename = thisfile[2:] 
             print "Inserting {} in ldm queue ".format(thisfilename)
             commandstr = "pqinsert -q /opt/ldm/var/queues/ldm.pq -f EXP {}".format(thisfilename)
             # test if the insertion was successful
             try:
                os.system(commandstr)
             except:
                print "ldm queue insertion failed. Removing: {}".format(thisfilename)
             # Now remove the converted file
             level2path = "{}/{}".format(workingDir,thisfilename) 
             print "Deleting: {}".format(level2path)
             try:
                os.remove(level2path)
             except OSError as e: # name the Exception `e`
                print "Failed with:", e.strerror # look what it says
                #print "Error code:", e.code 
             #except:
             #   print "Unable to remove: {}".format(level2path)
             #
    # a file without the OR_ABI prefix is unknown
    else:
       print "Unknown filename: {}".format(filepath)
    
    print "Removing: {}".format(filepath)
    try:
       os.remove(filepath)
    except:
       print "Unable to remove: {}".format(thisfilename)
    #
    endtime  = datetime.utcnow()
    print "End time: {}Z".format(endtime.strftime("%Y%m%d %H%M"))
    
    return

if __name__ == '__main__':
       # Now the file is uncompressed and renamed with the "Alaska_" prefix.
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
    main()
