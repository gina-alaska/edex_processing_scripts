#!/usr/bin/env /awips2/python/bin/python
"""Converts a NGFS heat points CSV file to an AWIPS netcdf file
   that can be read with the dmw plug-in. Ver: 2.0"""

import argparse
import shutil
from shutil import copy, copyfileobj
import os
import netCDF4
import sys
import random
import json
#import pandas
import datetime
from datetime import datetime,timedelta
from time import strftime,strptime
import numpy as np

##############################################################
# read command line arguments and sets 

def _process_command_line():
    """Process the command line arguments.
    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )
    parser.add_argument(
        '-r', '--readonly', action='store_true', help='Read h5 file and report'
    )
    parser.add_argument(
        '-s', '--srcdir', action='store', default='one',
        help='CSV file source'
    )
    parser.add_argument(
        '-f', '--filepath', action='store', required=True,
        help='CSV file path'
    )
    parser.add_argument('--version', action='version', version='%(prog)s ver:2.0')
    args = parser.parse_args()
    return args

##############################################################
# create a new pathname for the netcdf file using segments of the
# input file name

def getnewpath(filepath,datestr,satname,srcdir):

    #filename = os.path.basename(filepath)
    dirname = os.path.dirname(filepath)
    if len(dirname) == 0:
       dirname = '.'
    # generate a random number to add to the filename and make them unique
    rnum = random.randrange(1,10000,1)
    ## now create the new filename 
    newfname = "{}/UAF_ngfsdmw_GWFD_fires_{}_{}_{}_{:05d}.nc".format(dirname,satname,srcdir,datestr,rnum)
    return newfname

###############################################################
# read appropriate variables from the .csv file

def read_json_file(filepath,lat,lon,frp,conf,fcode,PA,qual,wfo,acqtime,pixtime):

   f =  open(filepath)
   data = json.load(f)
   numpts = 0
   for feature in data['features']:
      prop = feature['properties']
      lat.append(float(prop['latitude']))
      lon.append(float(prop["longitude"]))
      acqtime.append(datetime.strptime(prop["acq_date_time"],"%Y-%m-%dT%H:%M:%SZ"))
      pixtime.append(datetime.strptime(prop["pixel_date_time"],"%Y-%m-%dT%H:%M:%SZ"))
      #actime = prop['acq_date_time']
      #pixime = prop['pixel_date_time']
      frp.append(float(prop["frp"])+.0011)  # FRP value
      #confstr = prop['confidence']
      if prop["confidence"] == "nominal":  #confidence value
         conf.append(8)
      else:
         conf.append(7)
      satellite = prop["satellite"]
      PA.append(float(prop["type"]))  # persistent anomaly type
      fcode.append(float(prop["nws_fire_wx_code"]))  # NWS fire wx action code
      qual.append(float(prop["quality_flag"]))  # quality assessment of the detection
      # Associated WFO
      if (prop["nws_wfo_code"] == 'NULL' or prop["nws_wfo_code"] == 'Unknown' or prop["nws_wfo_code"] == ''):
         wfo.append("MISG")
      else:
         wfo.append(prop["nws_wfo_code"])
      numpts += 1 
   #except csv.Error as e:
   #   sys.exit('file: {}, line: {} ... {}',format(csvfile, reader.line_num, e))
   f.close()
   if numpts == 0:
       sys.exit('No valid detections found.')
     
   return(acqtime,pixtime,satellite,numpts,lat,lon,frp,conf,fcode,PA,qual,wfo)

###############################################################
# write all the numpy data to a netcdf file and add the needed
# global and variable attributes

def write_ngfsfires_ncfile(filepath,sdate,edate,satname,numpts,lat,lon,frp,conf,fcode,PA,qual,wfo):

    #sat_dict = {"GOES-18":"ABI_GOES-West",'SNPP':"VIIRS",'npp':'S-NPP'}
    try:
       ncfh = netCDF4.Dataset(filepath, 'w', format='NETCDF4')
    except IOError:
       print ('Error opening {}').format(filepath)
       raise SystemExit
    except OSError:
       print ('Error accessing {}').format(filepath)
       raise SystemExit

    #debug output
    #print "Latitude:",lat
    #print "Longitude:",lon
    #print "Dim:{}".format(numpts)

    # set dimensions
    fdimid = ncfh.createDimension('nfire', None)
    dmwdimid = ncfh.createDimension('dmw_band', 1)
    # set global attributes
    #setattr(ncfh, "_NCProperties", "version=2,netcdf=4.7.4,hdf5=1.10.5")
    if satname == 'GOES-18':
       setattr(ncfh, "mission_name", "ABI_GOES-West")
       setattr(ncfh, "scene", "Full-Disk_NGFS")
    else:
       setattr(ncfh, "mission_name", "VIIRS")
       setattr(ncfh, "scene", "Full-Disk")
    setattr(ncfh, "ngfs_source", satname)
    sdatestr = sdate[0].strftime("%Y-%m-%dT%H:%M:%S.0.Z")
    setattr(ncfh, "first_meas_time", sdatestr)
    edatestr = edate[0].strftime("%Y-%m-%dT%H:%M:%S.0.Z")
    setattr(ncfh, "last_meas_time", sdatestr)
    setattr(ncfh, "production_site", "UAF")
  
    # create variables
    latvar = ncfh.createVariable('latitude','f8','nfire')
    latvar.units = 'degrees_ndatetime.orth'
    latvar.long_name = 'latitude'
    lonvar = ncfh.createVariable('longitude','f8','nfire')
    lonvar.units = 'degrees_east'
    lonvar.long_name = 'longitude'
    frpvar = ncfh.createVariable('frp_ngfs','f4','nfire')
    frpvar.units = 'MW'
    frpvar.long_name = 'Fire radiative power' 
    confvar = ncfh.createVariable('FP_confidence','f4','nfire')
    confvar.units = '%'
    confvar.long_name = 'Detection confidence' 
    PAvar = ncfh.createVariable('type_ngfs','f4','nfire')
    PAvar.units = '1'
    PAvar.long_name = 'persistent industrial or nature source, 0 none, 1 oil or gas, 2 volcano, 3 solar panel, 4 urban, 5 unclassified' 
    tmvar = ncfh.createVariable('time_ngfs','f8','nfire')
    tmvar.units = 's'
    tmvar.long_name = 'NGFS time_coverage_start as array'
    DQFvar = ncfh.createVariable('DQF_ngfs','f8','nfire')
    DQFvar.units = '1'
    DQFvar.long_name = 'Delineator of zero vs non zero FP_Confidence'
    DQFvar.flag_values = 0, 1
    DQFvar.flag_meanings = 'FP_confidence is gt zero, FP_confidence is eq to zero"'
    dmwvar = ncfh.createVariable('band_id','b','dmw_band')
    dmwvar.longname = 'Generic band identifier for use in AWIPS dmw plugin'
    dmwvar.units = '1'
    fcodevar = ncfh.createVariable('nws_fire_wx_code_ngfs','f4','nfire')
    fcodevar.longname = 'NWS fire weather code'
    fcodevar.units = '1'
    qualvar = ncfh.createVariable('quality_flag','f4',('nfire'))
    qualvar.longname = 'Detection quality flag'
    qualvar.units = '1'
    wfovar = ncfh.createVariable('wfo_id','str',('nfire'))
    wfovar.longname = 'NWS WFO AOR'
 
    #now write to the data arrays
    latvar[:] = lat
    lonvar[:] = lon
    frpvar[:] = frp
    confvar[:] = conf
    fcodevar[:] = fcode
    PAvar[:] = PA
    qualvar[:] = qual 
    for i in range(numpts):
       wfovar[i] = wfo[i]

    #set time in unix secs...dqflags...persistent anomalies
    secs = []
    dqf = []
    #print("date={}".format(dateobj.datestrftime("%y-%m-%d-%H-%M")))
    for i in range(0,numpts):
       secs.append(sdate[i].strftime("%s"))
       dqf.append(0)
       if conf[i] == 0:
          dqf = 1
    # 
    tmvar[:] = secs 
    DQFvar[:] = dqf
    dmw = 99
    dmwvar[:] = dmw

    ncfh.close()

##############################################################
def main():
    """Call to run script."""
    args = _process_command_line()
    if not os.path.exists(args.filepath):
        print ("File not found: {}").format(args.filepath)
        raise SystemExit
   
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
    filepath = args.filepath
    sdate,edate,satname,numpts,lat,lon,frp,conf,fcode,PA,qual,wfo = read_json_file(filepath,lat,lon,frp,conf,fcode,PA,qual,wfo,sdate,edate)
    if numpts == 0:
       print ("No points found")
       return   
    else:
       if args.verbose:
          print ("Fire points: {}".format(numpts))
    # Determine the new netcdf filepath for containing the data
    datestr = sdate[0].strftime("%Y%m%dT%H%M%S")
    newfilepath = getnewpath(filepath,datestr,satname,args.srcdir)
    if args.verbose:
       print ("New file: {}".format(newfilepath))

    if args.verbose:
       print ("Latitude: {} Longitude: {}  FRP: {}".format(lat,lon,frp))

    if args.readonly:
       print ("No conversion requested. Reporting output...")
       # all the points
       for i in range(numpts):
          print("sdate={}  lat={} lon={} FRP={}".format(sdate[i].strftime("%Y-%m-%dT%H:%M:%S"), lat[i], lon[i], frp[i]))
          print("wfo action code={}",format(fcode[i]))
    else:
       # write to the new file
       write_ngfsfires_ncfile(newfilepath,sdate,edate,satname,numpts,lat,lon,frp,conf,fcode,PA,qual,wfo)
       print ("Converted file: {}".format(newfilepath))
       if args.verbose:
          print ("done")
    return

if __name__ == '__main__':
    # this is only executed if the script is run from the command line
    main()
