#!/usr/bin/env /awips2/python/bin/python
"""Get all the files in datastore netcdf file."""

import argparse
import os, sys
import gzip
from shutil import copy, move
import datetime
from datetime import datetime
import time
#sys.path.append('/home/awips/bin')
from ncConvertNGFS_json import write_ngfsfires_ncfile, read_json_file, getnewpath

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
    queueLimit = 60 
    # read command line
    args = _process_command_line()

    print ("------\n{}Z {}\nReceived: {}".format(curtime.strftime("%Y%m%d %H%M"), sys.argv[0], args.filepath))
    #
    # check to make sure file exists
    if not os.path.exists(args.filepath):
        print ("File not found: {}".format(args.filepath))
        raise SystemExit
    #
    filepath = args.filepath
    print ("Valid filepath: {}".format(filepath))
    #
    if "geojson" in filepath:
       # define empty lists
       lat = []
       lon = []
       frp = []
       conf = []
       PA = []
       fcode = []
       qual = []
       wfo = []
       sdate = []
       edate = []

       # read the CSPP i-band netcdf file
       sdate,edate,satname,numpts,lat,lon,frp,conf,fcode,PA,qual,wfo = read_json_file(filepath,lat,lon,frp,conf,fcode,PA,qual,wfo,sdate,edate)
       if numpts == 0:
          print ("No points found")
          return
       else:
          print ("Valid fire points = {}".format(numpts))
          if args.verbose:
             print ("New file: {}".format(newfilepath))
             print ("Fire points: {}".format(numpts))
             print ("Latitude: {} Longitude: {}  FRP: {}".format(lat,lon,frp))

       # Determine the new netcdf filepath for containing the data
       datestr = sdate[0].strftime("%Y%m%dT%H%M%S")
       newfilepath = getnewpath(filepath,datestr,satname,"one")

       # write to the new file
       write_ngfsfires_ncfile(newfilepath,sdate,edate,satname,numpts,lat,lon,frp,conf,fcode,PA,qual,wfo)
       print ("Converted file: {}".format(newfilepath))
       # move converted file to ingest
       print ("Moving {} to {}".format(newfilepath, ingestDir))
       try:
          move(newfilepath,ingestDir)
       except:
          print ("Move to ingest failed. Removing converted file: {}".format(newfilepath))
          print ("Removing: {}".format(newfilepath))

       print ("Removing: {}".format(filepath))
       os.remove(filepath)
    #
    # a file without a "geojson" suffix is unknown
    else:
       print ("Unrecognized file format: {}".format(filepath))
    #
    return

if __name__ == '__main__':
    main()
