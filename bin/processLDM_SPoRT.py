#!/usr/bin/env /awips2/python/bin/python
"""Get all the files in datastore netcdf file."""

import argparse
import os, sys, stat
import gzip
from shutil import copy, move
import datetime
from datetime import datetime
from Scientific.IO import NetCDF
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

def chg_attribute(ncpath, attname, attval, verbose):
    """Call to change a netcdf attribute."""

    if not os.path.exists(ncpath):
        print 'File not found: {}'.format(ncpath)
        raise SystemExit
    try:
        if verbose:
            print 'Opening {}'.format(ncpath)
        cdf_fh = NetCDF.NetCDFFile(ncpath, 'a')
    except IOError:
        print 'Error accessing {}'.format(ncpath)
        raise SystemExit
    except OSError:
        print 'Error accessing {}'.format(ncpath)
        raise SystemExit

    try:
        setattr(cdf_fh, attname, attval)
    except IOError:
        print 'Error accessing {}'.format(ncpath)
        raise SystemExit
    except OSError:
        print 'Error accessing {}'.format(ncpath)
        raise SystemExit
    print 'Attribute {} changed to {}'.format(attname, attval)
    cdf_fh.close()
    return

#####################################################################

def main():
    """Call to run script."""
    curtime  = datetime.utcnow()
    logpath="/opt/ldm/var/logs/edex-ingest-LDMsat-{}.log".format(curtime.strftime("%Y%m%d"))
    sys.stdout = sys.stderr = open(logpath, 'a+')

    queueLimit = 60 
    ingestDir = "/awips2/edex/data/manual"

    args = _process_command_line()

    print "-----\n{}Z Received: {}".format(curtime.strftime("%Y%m%d %H%M"), args.filepath)

    if not os.path.exists(args.filepath):
        print "File not found: {}".format(args.filepath)
        raise SystemExit

    filepath = args.filepath
    filenm = os.path.basename(filepath)
    print "Valid filepath: {}".format(filepath)

    ##################################
    # To stop data flow to AWIPS, uncomment these lines
    #os.remove(filepath)
    #print "Skipping ingest:{}".format(filepath)
    #raise SystemExit
    #
    ##################################
    # this section is only for support of remote file downloads (i.e. to carl)
    #queueDir = "/data_store/ldmqueue"
    #if not os.path.exists(queueDir):
    #   os.makedirs(queueDir)
    #   os.chmod(queueDir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    #fnum = len(os.listdir(queueDir))
    #if fnum < queueLimit:
    #   print "copying {} to {}".format(filepath, queueDir)
    #   copy(filepath,queueDir)
    #   quefilepath = '{}/{}'.format(queueDir, filenm)
    #   os.chmod(quefilepath, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    #else:
    #   print "Skip copy. Too many files in queue: {}".format(fnum)
    ##################################
    prodnames = ['dust.nc','ash.nc','ntmicro.nc','color.nc','airmass.nc','false.nc']
    # look for ".gz" in file path to indicate compression is needed
    if ".gz" in filepath:
       dirnm = os.path.dirname(filepath)
       basenm = os.path.splitext(filenm)[0]
       #nameseg=basenm.split('_')
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
       # after redirected compression the compressed file needs to be removed
       os.remove(filepath)
       # set the filepath to point to the uncompresses name
       filepath = newfilepath
       #
       # Now the file is uncompressed and renamed with the "Alaska_" prefix.
       #############################################
       # This section is for future tweaks that may be needed (like netcdf attributes).
       if "sfr.nc" in filepath:
          print "Changing satelliteName to NESDIS POES in file: {}".format(filepath)
          chg_attribute(filepath, "satelliteName", "NESDIS POES", args.verbose)
       elif "viirs_alaska" in filepath:
          if any([x in filepath for x in prodnames]):
             print "Changing satelliteName to SPORT VIIRS in file: {}".format(filepath)
             chg_attribute(filepath, "satelliteName", "SPoRT VIIRS", args.verbose)
       elif "modis_alaska" in filepath:
          if any([x in filepath for x in prodnames]):
             print "Changing satelliteName to SPORT MODIS in file: {}".format(filepath)
             chg_attribute(filepath, "satelliteName", "SPoRT MODIS", args.verbose)
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
