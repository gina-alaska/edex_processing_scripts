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

    print "------\n{}Z Received: {}".format(curtime.strftime("%Y%m%d %H%M"), args.filepath)
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
    ################################################
    # this section is only for support of remote file downloads (i.e. by carl)
    if "RIVER" in filepath:
       queueDir = "/data_store/ldmqueue"
       if not os.path.exists(queueDir):
          os.makedirs(queueDir)
          os.chmod(queueDir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
       fnum = len(os.listdir(queueDir))
       if fnum < queueLimit:
          print "copying {} to {}".format(filepath, queueDir)
          copy(filepath,queueDir)
          quefilepath = '{}/{}'.format(queueDir, filenm)
          os.chmod(quefilepath, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
       else:
          print "Skip copy. Too many files in queue: {}".format(fnum)
    ################################################

    # look for "SSEC" in file path to indicate compression is needed even tho ".gz" is missing
    if "SSEC" in filepath:
       # determine the filepath directory and base names
       dirnm = os.path.dirname(filepath)
       basenm = os.path.splitext(filenm)[0]
       # use the directory and base to create a new name with "Alaska" prefix and ".nc" extension
       if ".nc" in basenm:
          newfilepath="{}/Alaska_{}".format(dirnm, basenm)
       else:
          newfilepath="{}/Alaska_{}.nc".format(dirnm, basenm)
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
       # Now the file is uncompressed and renamed with the "Alaska_" prefix.
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
       # 
       ##############################################
       #
       # OK, ready to move the file to the ingest directory
       print "Moving {} to {}".format(filepath, ingestDir)
       move(filepath,ingestDir)
       #
    # a file with a UAF prefix and no ".gz" extension is unknown
    else:
       print "Unrecognized file format: {}".format(filepath)
    #
    return

if __name__ == '__main__':
    main()
