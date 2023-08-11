#!/awips2/python/bin/python3
"""Get all the files in datastore netcdf file."""
import argparse
import os
from datetime import datetime, timedelta

satellites = {
    "terra": "terra",
    "aqua": "aqua",
    "noaa21": "noaa21",
    "noaa20": "noaa20",
<<<<<<< HEAD
=======
    "n20": "n20",
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
    "noaa19": "noaa19",
    "noaa18": "noaa18",
    "metopc": "metopc",
    "metopb": "metopb",
<<<<<<< HEAD
    "n21": "noaa21",
    "N21": "noaa21",
    "n20": "noaa20",
    "j01": "noaa20",
    "n19": "noaa19",
    "n18": "noaa18",
    "npp": "s-npp",
    "moc": "metopc",
    "mob": "metopb",
    "ma3": "metopc",
    "ma1": "metopb",
    "GW1": "amsr2",
=======
    "npp": "s-npp",
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
}

def _process_command_line():
    """Process the command line arguments.
    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day', action='store', help='day of month to search')
    parser.add_argument('-t', '--type', action='store', default='regionalsat', help='type of file (goesr, grib, nucaps, regionalsat)')
    parser.add_argument('-m', '--match', action='store', help='string pattern to match')
<<<<<<< HEAD
    parser.add_argument('-n', '--nws', action='store_true', help='use nws archivedirectory')
    parser.add_argument('-e', '--exclude', action='store', help='string pattern to exclude')
=======
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
    parser.add_argument('-lo', '--latencyonly', action='store_true', help='show latency summary')
    parser.add_argument('-fl', '--filelatency', action='store_true', help='compare file date and time stamp')
    parser.add_argument('-po', '--passesonly', action='store_true', help='show pass time, satellite, and sensor only')
    parser.add_argument('-s', '--tstamp', action='store_true', help='show time stamps only')
    parser.add_argument('-b', '--abbrev', action='store_true', help='abbreviate results')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose flag')
<<<<<<< HEAD
    args = parser.parse_args()
    return args


=======
    parser.add_argument('-e', '--exclude', action='store', help='string pattern to exclude')
    args = parser.parse_args()
    return args

>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
def getvalidtime(path, ftype, verbose):
     """ extract the valid date and time from the filename. """
     fname = os.path.basename(path)
     fparts=fname.split('_')
     vsecs = 0
     dtstr = ""
     satellite = ""
     sensor = ""
     fplen = len(fparts)
     if ftype == "goesr":
        ### SCMI DB Imagery (VIIRS, MODIS, AVHRR)
        if "Polar" in path:
           idx = fparts.index("Polar")
           datestr = fparts[idx+2]
           timestr = fparts[idx+3]
<<<<<<< HEAD
           vsecs, dtstr = parse_file_time(datestr, timestr,4)
           satellite, sensor = get_sat_sensor(path, fparts)
        ### GOES-18 from Unidata
        elif "G18" in path:
           idx = fparts.index("G18")
           ## date string has day of year instead of month & day
           datestr = fparts[idx+1] 
=======
           vyr = int(datestr[:4])
           vmo = int(datestr[4:6])
           vda = int(datestr[6:8])
           vhr = int(timestr[0:2])
           vmn = int(timestr[2:4])
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
           for keyword, value in satellites.items():
                if keyword in path:
                    idx = fparts.index(keyword)
                    satellite = fparts[idx]
                    sensor = fparts[idx+1]
                    if satellite == "n20":
                        satellite = "noaa20"
                    break
        elif "G18" in path:
           idx = fparts.index("G18")
           datestr = fparts[idx+2]
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
           vyr = int(datestr[1:5])
           vjd = int(datestr[5:8])
           vhr = int(datestr[8:10])
           vmn = int(datestr[10:12])
           tmpdate=datetime(vyr, 1, 1) + timedelta(vjd-1)
           vmo = int(tmpdate.strftime("%m"))
           vda = int(tmpdate.strftime("%d"))
           vtime = datetime(vyr, vmo, vda, vhr, vmn)
           vsecs = int(vtime.strftime("%s"))
           dtstr = vtime.strftime("%y%m%d_%H%M")
           satellite = "goes-18"
           sensor = "abi"
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
<<<<<<< HEAD
     ### Regionalsat format for special products
=======
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
     elif ftype == "regionalsat":
        if "sport" in path:      ### sport microwave products
           idx = fparts.index("sport")
           datestr = fparts[idx-2]
           timestr = fparts[idx-1]
           vsecs,dtstr = parse_file_time(datestr, timestr,4)
           satellite = "noaa"
           sensor = "microwave"
        elif "VSCD-AK" in path:  ### CIRA SnowCloud Discriminator
           idx = fparts.index("VIIRS")
           datestr = fparts[idx+1]
           timestr = fparts[idx+2]
           vsecs,dtstr = parse_file_time(datestr, timestr,2)
           satellite = "noaa"
           sensor = "viirs"
        elif "OMPS-AK" in path:  ### OMPS Products
           idx = fparts.index("1KM")
           datestr = fparts[idx+2]
           timestr = fparts[idx+3]
           vsecs,dtstr = parse_file_time(datestr, timestr,2)
           satellite = "noaa"
           sensor = "omps"
        elif "VIIRS-AK" in path: ### VIIRS Volcano Index products
           idx = fparts.index("1KM")
           datestr = fparts[idx+2]
           timestr = fparts[idx+3]
           vsecs,dtstr = parse_file_time(datestr, timestr,2)
           satellite = "noaa"
           sensor = "viirs"
        elif "RIVER" in path:    ### RiverFlood Products
           idx = fparts.index("1KM")
           datestr = fparts[idx+2]
           timestr = fparts[idx+3]
           vsecs,dtstr = parse_file_time(datestr, timestr,4)
           satellite = "noaa"
           sensor = "viirs"
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, fname))
           vsecs = 0
           dtstr = ""
     ### Pointset data type for Microwave products
     elif ftype == "pointset":
        if "v2r2" in path:       ### AMSR2 and SFR products
           idx = fparts.index("v2r2")
           datestr = fparts[idx+2][1:9]
           timestr = fparts[idx+2][9:13]
           vsecs,dtstr = parse_file_time(datestr, timestr,4)
           satellite, sensor = get_sat_sensor(path, fparts)
           sensor = "microwave"
        elif "v11r8" in path:    ### MIRS products
           idx = fparts.index("v11r8")
           datestr = fparts[idx+2][1:9]
           timestr = fparts[idx+2][9:13]
           vsecs,dtstr = parse_file_time(datestr, timestr,4)
           satellite, sensor = get_sat_sensor(path, fparts)
           sensor = "microwave"
        elif "v3r0" in path:    ### VIIRS JRR products
           idx = fparts.index("v3r0")
           datestr = fparts[idx+2][1:9]
           timestr = fparts[idx+2][9:13]
           vsecs,dtstr = parse_file_time(datestr, timestr,4)
           satellite, sensor = get_sat_sensor(path, fparts)
           sensor = "microwave"
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     ### CMORPH2 data on LatLon Grid
     elif ftype == "netcdfGrid":
        if "CMORPH2" in path:
           idx = fparts.index("0.05deg-30min")
           datestr = fparts[idx+1][:8]
           timestr = fparts[idx+1][8:12]
           vsecs,dtstr = parse_file_time(datestr, timestr,4)
           satellite = "multiple"
           sensor = "microwave"
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, fname))
           vsecs = 0
           dtstr = ""   
     ### VIIRS Active Fire Detections
     elif ftype == "dmw":
        if "UAF" in path: 
         idx = fparts.index("UAF")
         datestr = fparts[idx+4]  
         timestr = fparts[idx+4][9:13] 
         vsecs,dtstr = parse_file_time(datestr, timestr,4)
         satellite = fparts[idx+3]
         sensor = fparts[idx+1]
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     ### MIMIC TPW from CIMSS
     elif ftype == "grib": 
        if "TPW" in path: 
         idx = fparts.index("TPW")
         datestr = fparts[idx+1]  
         timestr = fparts[idx+2] 
         vsecs,dtstr = parse_file_time(datestr, timestr,4)
         satellite = "multiple"
         sensor = "microwave"
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     ### DB NUCAPS from HEAP
     elif ftype == "griddednucaps":  
        if "KNES" in path:
         idx = fparts.index("KNES")
         dir = path.split("/")
         diridx = dir.index("griddednucaps")
         subdirdatestr = dir[diridx + 1] 
         datestr = subdirdatestr  
         timestr = fparts[idx+1][2:6] 
         vsecs,dtstr = parse_file_time(datestr, timestr,4)
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     ### DB NUCAPS from HEAP if not gridded
     elif ftype == "nucaps":
<<<<<<< HEAD
        if "KNES" in path:
           idx = fparts.index("KNES")
           dir = path.split("/")
           diridx = dir.index("nucaps")
           subdirdatestr = dir[diridx + 1] 
           datestr = subdirdatestr  
           timestr = fparts[idx+1][2:6] 
           vsecs,dtstr = parse_file_time(datestr, timestr,4)
=======
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
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
<<<<<<< HEAD
     return (vsecs, dtstr, satellite, sensor)


def parse_file_time(datestr, timestr,yrlen):
     if yrlen == 4:
         vyr = int(datestr[:4]) 
         vmo = int(datestr[4:6]) 
         vda = int(datestr[6:8])
     elif yrlen == 2: 
         vyr = int(datestr[:2]) + 2000
         vmo = int(datestr[2:4]) 
         vda = int(datestr[4:6])
     vhr = int(timestr[:2])
     vmn = int(timestr[2:4])
     vtime = datetime(vyr, vmo, vda, vhr, vmn)
     vsecs = int(vtime.strftime("%s"))
     dtstr = vtime.strftime("%y%m%d_%H%M")
     return (vsecs, dtstr)


def get_sat_sensor(path, fparts):
     for keyword, value in satellites.items():
          if keyword in path:
             satellite = value
             idx = fparts.index(keyword)
             sensor = fparts[idx+1]
             return (satellite, sensor)
     return ("unknown", "unknown")


=======
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
     elif ftype == "dmw":
        if "UAF" in path: 
         idx = fparts.index("UAF")
         datestr = fparts[idx+4]  
         timestr = fparts[idx+4] 
         vyr = int(datestr[:4]) 
         vmo = int(datestr[4:6]) 
         vda = int(datestr[6:8])
         vhr = int(timestr[9:11])
         vmn = int(timestr[11:13])
         vtime = datetime(vyr, vmo, vda, vhr, vmn)
         vsecs = int(vtime.strftime("%s"))
         dtstr = vtime.strftime("%y%m%d_%H%M")
         satellite = fparts[idx+3]
         sensor = fparts[idx+1]
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     elif ftype == "grib": 
        if "TPW" in path: 
         idx = fparts.index("TPW")
         datestr = fparts[idx+1]  
         timestr = fparts[idx+2] 
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
     elif ftype == "griddednucaps":  
        if "KNES" in path:
         idx = fparts.index("KNES")
         dir = path.split("/")
         diridx = dir.index("griddednucaps")
         subdirdatestr = dir[diridx + 1] 
         datestr = subdirdatestr  
         timestr = fparts[idx+1] 
         vyr = int(datestr[:4]) 
         vmo = int(datestr[4:6]) 
         vda = int(datestr[6:8])
         vhr = int(timestr[2:4])
         vmn = int(timestr[4:6])
         vtime = datetime(vyr, vmo, vda, vhr, vmn)
         vsecs = int(vtime.strftime("%s"))
         dtstr = vtime.strftime("%y%m%d_%H%M")
        else:
           if verbose:
              print ("Unknown {} file: {}".format(ftype, path))
           vsecs = 0
           dtstr = ""
     return (vsecs, dtstr, satellite, sensor)

#def get_passes_by_type(path, ddttstr, sat, snsr, passes):
#    """Get passes for a specific file type and date."""
#    args = _process_command_line()
#    date = str(ddttstr)[:6]
#    time = str(ddttstr)[7:]
#    if sat:
#        if args.match is None:
#            format_pass = f"{date}\t{time}  {sat}\t {snsr}\n"
#            passes.append(format_pass)
#        elif args.match.startswith(f"{snsr}_"):
#            format_pass = f"{date}\t{time}  {sat}\t {snsr}\n"
#            passes.append(format_pass)
#        elif args.match == snsr:
#            format_pass = f"{date}\t{time}  {sat}\t {snsr}\n"
#            passes.append(format_pass)
#    return passes

>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
def format_pass(path, ddttstr, sat, snsr):
    """Get passes for a specific file type and date."""
    date = str(ddttstr)[:6]
    time = str(ddttstr)[7:]
    format_pass = f"{date}\t{time}  {sat}\t {snsr}\n"
    return format_pass


<<<<<<< HEAD
def get_filepaths(directory,altpathflag):
=======
def get_filepaths(directory):
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
    """Generate the filenames in a directory tree by walking down the tree."""
    file_paths = []
    if altpathflag:
       for root, directories, files in os.walk(directory):
           if "GINA" in root:
              for filename in files:
                 # Join the two strings to form the full path
                 filepath = os.path.join(root,filename)
                 file_paths.append(filepath)

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def main():
    """Call to run script."""
    basedirectory = "/data_store/manual"
    passes = []
    args = _process_command_line()
<<<<<<< HEAD
    altpathflag = 0
    if args.nws:
       basedirectory = "/data_store/sat"
       altpathflag = 0
        
=======
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
    searchpath = "{}/{}".format(basedirectory, args.type)
    curtime = datetime.utcnow()
    if args.day is not None:
        if int(args.day) > 31:
            dom = int(args.day) % 100
            mon = int(args.day) / 100
            subDir = '{}{:02}{:02}'.format(curtime.strftime("%Y"), mon, dom)
        else:
            subDir = '{}{:02}'.format(curtime.strftime("%Y%m"), int(args.day))
<<<<<<< HEAD
        paths = get_filepaths('{}/{}'.format(searchpath, subDir), altpathflag)
    else:
        subDir = curtime.strftime("%Y%m%d")
    print(subDir)
    paths = get_filepaths('{}/{}'.format(searchpath, subDir), altpathflag)
=======
        paths = get_filepaths('{}/{}'.format(searchpath, subDir))
    else:
        subDir = curtime.strftime("%Y%m%d")
    print(subDir)
    paths = get_filepaths('{}/{}'.format(searchpath, subDir))
>>>>>>> 1c9d57602131d49629efe5254a5c0dcaca5f1b09
    paths.sort(reverse=True)
    count = 0
    unknown = 0
    sumlatency = 0
    maxlatency = 0
    minlatency = 2000
    file_times = []
    total_size = 0
    unique_passes = set()
    for path in paths:
        savesecs = os.path.getmtime(path)
        savetime = datetime.fromtimestamp(savesecs)
        validsecs, ddttstr, sat, snsr = getvalidtime(path, args.type, args.verbose)
        latency = int((savesecs - validsecs) / 60)
        ####passes = get_passes_by_type(path, ddttstr, sat, snsr, passes)
        ####sorted_passes = sorted(passes)  # Sort the passes list in ascending order
        if args.match:
            if args.match not in path:
                continue
        if args.exclude:
            if args.exclude in path:
                continue
        file_stats = os.stat(path)
        total_size += file_stats.st_size
        if args.filelatency:
            print("{:d}m\t{}".format(latency, path))
        elif args.tstamp:
            if ddttstr not in file_times:
                file_times.append(ddttstr)
        elif args.passesonly:
            passes.append(format_pass(path, ddttstr, sat, snsr))
                ####unique_passes.update(sorted_passes)  # Use update instead of sorted_passes
        else:
            if not args.latencyonly:
                print("{}".format(path))
        if validsecs > 0:
            sumlatency += latency
            if latency > maxlatency:
                maxlatency = latency
            if latency < minlatency:
                minlatency = latency
            count += 1
        else:
            unknown += 1
    if args.latencyonly:
        pass
    if args.passesonly:
        unique_passes = sorted(set(passes))  # Sort passes and make unique
        if unique_passes:
            print("\n Date\tTime  Satellite  Sensor")
            print("------\t----  ---------  ------")
            print(''.join(unique_passes))
    if count > 0:
        file_times.sort()
        if args.tstamp and not args.abbrev:
          print("\n Date\tTime")
          print("------\t----")
          for ddttstr in file_times:
               print(f"{ddttstr[:6]}  {ddttstr[7:]}".format(file_times))
        avglatency = sumlatency / count
        total_gigabytes = total_size / 1073741824
        print("Products found: {}".format(count))
        print("Total file size: {:.2f} GB".format(total_gigabytes))
        print("Average latency: {:.1f} min".format(avglatency))
        print("Maximum latency: {:d} min".format(maxlatency))
        print("Minimum latency: {:d} min".format(minlatency))
    else:
        print("Nothing matches criteria.")
        if unknown > 0:
            print("Unknown products: {}".format(unknown))
            
if __name__ == '__main__':
    main()
