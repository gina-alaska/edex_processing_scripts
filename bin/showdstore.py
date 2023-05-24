#!/usr/bin/env python
"""Get all the files in datastore netcdf file."""

import argparse
import os
import datetime
from datetime import datetime
from datetime import timedelta
import time

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--day', action='store', help='day of month to search'
    )
    parser.add_argument(
        '-t', '--type', action='store', default='regionalsat', \
        help='type of file (goesr, grib, nucaps, regionalsat)'
    )
    parser.add_argument(
        '-m', '--match', action='store', help='string pattern to match'
    )
    parser.add_argument(
        '-l', '--latency', action='store_true', help='compare file dat and time stamp'
    )
    parser.add_argument(
        '-s', '--tstamp', action='store_true', help='show time stamps only'
    )
    parser.add_argument(
        '-b', '--abbrev', action='store_true', help='abbreviate results'
    )
    parser.add_argument(
       '-v', '--verbose', action='store_true', help='verbose flag'
    )
    args = parser.parse_args()
    return args

#####################################################################
def getvalidtime(path, ftype, verbose):
     """ extract the valid date and time from the filename. """
     fname = os.path.basename(path)
     fparts=fname.split('_')
     fplen = len(fparts)
     #for part in fparts:
     #   print part
     #print "Type: {}".format(ftype)
     if ftype == "goesr":
        if "Polar" in path:
           idx = fparts.index("Polar")
           datestr = fparts[idx+2]
           timestr = fparts[idx+3]
           vyr = int(datestr[:4])
           vmo = int(datestr[4:6])
           vda = int(datestr[6:8])
           vhr = int(timestr[0:2])
           vmn = int(timestr[2:4])
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
        elif "G17" in path:
           idx = fparts.index("G17")
           datestr = fparts[idx+2]
           vyr = int(datestr[1:5])
           vjd = int(datestr[5:8])
           vhr = int(datestr[8:10])
           vmn = int(datestr[10:12])
           tmpdate=datetime(vyr, 1, 1) + timedelta(vjd-1)
           vmo = int(tmpdate.strftime("%m"))
           vda = int(tmpdate.strftime("%d"))
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           #print "{}/{}/{}/{}/{}".format(vyr,vmo,vda,vhr,vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     elif ftype == "regionalsat":
        if "sport" in path:
           idx = fparts.index("sport")
           datestr = fparts[idx-2]
           timestr = fparts[idx-1]
           vyr = int(datestr[:4])
           vmo = int(datestr[4:6])
           vda = int(datestr[6:8])
           vhr = int(timestr[0:2])
           vmn = int(timestr[2:4])
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
        elif "VSCD-AK" in path:
           idx = fparts.index("VIIRS")
           datestr = fparts[idx+1]
           timestr = fparts[idx+2]
           vyr = int(datestr[:2]) + 2000
           vmo = int(datestr[2:4])
           vda = int(datestr[4:6])
           vhr = int(timestr[0:2])
           vmn = int(timestr[2:4])
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
        elif "RIVER" in path:
           idx = fparts.index("1KM")
           datestr = fparts[idx+2]
           timestr = fparts[idx+3]
           vyr = int(datestr[:4])
           vmo = int(datestr[4:6])
           vda = int(datestr[6:8])
           vhr = int(timestr[0:2])
           vmn = int(timestr[2:4])
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     elif ftype == "nucaps":
        pathparts=path.split('/')
        pdx = pathparts.index("nucaps")
        datestr = pathparts[pdx+1]
        idx = fparts.index("KNES")
        timestr = fparts[idx+1]
        vyr = int(datestr[:4])
        vmo = int(datestr[4:6])
        vda = int(datestr[6:8])
        vhr = int(timestr[2:4])
        vmn = int(timestr[4:6])
        vtime = datetime(vyr, vmo, vda, vhr, vmn)
        vsecs = int(vtime.strftime("%s"))
        dtstr = vtime.strftime("%y%m%d_%H%M")
     elif ftype == "pointset":
        if "v2r2" in path:
           idx = fparts.index("v2r2")
           datestr = fparts[idx+2]
           vyr = int(datestr[1:5])
           vmo = int(datestr[5:7])
           vda = int(datestr[7:9])
           vhr = int(datestr[9:11])
           vmn = int(datestr[11:13])
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     elif ftype == "netcdfGrid":
        if "CMORPH2" in path:
           idx = fparts.index("0.05deg-30min")
           datestr = fparts[idx+1]
           vyr = int(datestr[:4])
           vmo = int(datestr[4:6])
           vda = int(datestr[6:8])
           vhr = int(datestr[8:10])
           vmn = int(datestr[10:12])
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     else:
        if verbose:
           print ("Unknown {} file: {}".format(ftype, path))
        vsecs = 0
        dtstr = ""
     return(vsecs,dtstr)
     
#####################################################################
def get_filepaths(directory):
    """ generate the filenames in a directory tree by walking down
    the tree. """

    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
           # Join the two strings to form the full path
           filepath = os.path.join(root,filename)
           file_paths.append(filepath)

    return file_paths

#####################################################################

def main():
    """Call to run script."""
    basedirectory = "/data_store/manual"

    args = _process_command_line()
    searchpath = "{}/{}".format(basedirectory,args.type)

    curtime  = datetime.utcnow()
    if args.day is not None:
        if int(args.day) > 31:
           dom = int(args.day) % 100
           mon = int(args.day) / 100
           subDir = '{}{:02}{:02}'.format(curtime.strftime("%Y"),mon,dom)
        else:
           subDir = '{}{:02}'.format(curtime.strftime("%Y%m"),int(args.day))
        paths = get_filepaths('{}/{}'.format(searchpath,subDir))
    else:
        subDir = curtime.strftime("%Y%m%d")
    print (subDir)
    paths = get_filepaths('{}/{}'.format(searchpath,subDir))
    paths.sort(reverse=True)

    #if args.match:
    #   print "Matching {}".format(args.match)
    #
    count = 0
    unknown = 0
    sumlatency = 0
    maxlatency = 0
    minlatency = 2000
    file_times = []
    for path in paths:
       savesecs=os.path.getmtime(path)
       savetime=datetime.fromtimestamp(savesecs)
       validsecs,ddttstr = getvalidtime(path, args.type, args.verbose)
       latency = int((savesecs - validsecs) / 60)
       #HHMMstr = savetime.strftime("%H%M")
       if args.match:
          if args.match in path:
             if args.latency:
                print ("{:d}m {}".format(latency, path))
             elif args.tstamp:
                if ddttstr not in file_times:
                   file_times.append(ddttstr)
             else: 
                print ("{}".format(path))
             if validsecs > 0:
                sumlatency += latency
                if latency > maxlatency:
                   maxlatency = latency
                if latency < minlatency:
                   minlatency = latency
                count += 1
             else:
                unknown += 1
       else:
          if args.latency:
             print ("{:d}m {}".format(latency, path))
          elif args.tstamp:
             if ddttstr not in file_times:
                file_times.append(ddttstr)
          else: 
             print ("{}".format(path))
          if validsecs > 0:
             sumlatency += latency
             if latency > maxlatency:
                maxlatency = latency
             if latency < minlatency:
                minlatency = latency
             count += 1
          else:
             unknown += 1

    if count > 0:
       file_times.sort()
       if args.tstamp:
          if  not args.abbrev:
             for ddttstr in file_times:
                print ("{}".format(ddttstr))
       avglatency = sumlatency / count
       print ("Products found: {}".format(count))
       print ("Avg latency = {:.1f} min".format(avglatency))
       print ("Max latency = {:d} min".format(maxlatency))
       print ("Min latency = {:d} min".format(minlatency))
    else:
       print ("Nothing matches criteria.")
       if unknown > 0:
          print ("Unknown products: {}".format(unknown))

    return

if __name__ == '__main__':
    main()
