#!/usr/bin/env /awips2/python/bin/python
"""Get all the files in datastore netcdf file."""

import argparse
import os, sys
import gzip
from shutil import copy, move
import datetime
from datetime import datetime, timedelta
import time
from nucaps4awips import fix_nucaps_file

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
    tmpDir = "/data_store/download"
    ingestDir = "/awips2/edex/data/manual"

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

    filepath = args.filepath
    os.chdir(tmpDir)

    # look for ".gz" in file path to indicate compression is needed
    if ".gz" in filepath:
       # determine the filepath directory and base names
       dirnm = os.path.dirname(filepath)
       filenm = os.path.basename(filepath)
       basenm = os.path.splitext(filenm)[0]
       # use the directory and base to create a new name with "Alaska" prefix and ".nc" extension
       if ".nc" in basenm:
          newfilepath="{}/{}".format(dirnm, basenm)
       else:
          newfilepath="{}/{}.nc".format(dirnm, basenm)
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
    if ".nc" in filepath:
       print "fix nucaps file"
       newfilename = fix_nucaps_file(filepath)
       print "new filename = {}".format(newfilename)
       newfilepath = "{}/{}".format(tmpDir,newfilename)
       if os.path.exists(newfilepath):
          # a new converted file has been made so remove the original file
          print "Removing: {}".format(filepath)
          os.remove(filepath)
       else:
          print "Conversion failed: {}".format(filepath)
          raise SystemExit
          
       # assign filepath to the new converted file
       filepath = newfilepath
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
       # 
       ##############################################
       #
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
       # Now the file is uncompressed and renamed with the "Alaska_" prefix.
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
    main()
