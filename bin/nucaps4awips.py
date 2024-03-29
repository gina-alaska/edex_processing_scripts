#!/usr/bin/env /awips2/python/bin/python
"""Get and set attributes on a satellite netcdf file. Ver: 1.3"""

import argparse
import shutil
from shutil import copy, copyfileobj
import os
import h5py
import sys
import numpy as np
# import numpy

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )
    parser.add_argument(
        '-f', '--filepath', action='store', required=True,
        help='netCDF file path'
    )
    args = parser.parse_args()
    return args

##############################################################3
def wmo_header_block(clat, clon):

    if ( -35.0 <= clat < 37.0 and 270.0 <= clon <= 325.0 ):
          wmostr="IUTN01"
    elif ( 37.0 <= clat <= 75.0 and 270.0 <= clon <= 325.0 ):
          wmostr="IUTN02"
    elif ( -35.0 <= clat < 37.0 and 251.0 <= clon < 270.0 ):
          wmostr="IUTN03"
    elif ( 37.0 <= clat <= 75.0 and 251.0 <= clon < 270.0 ):
          wmostr="IUTN04"
    elif ( -35.0 <= clat < 42.0 and 220.0 <= clon < 251.0 ):
          wmostr="IUTN05"
    elif ( 42.0 <= clat <= 75.0 and 232.0 <= clon < 251.0 ):
          wmostr="IUTN06"
    elif ( 42.0 <= clat < 52.0 and 220.0 <= clon < 232.0 ):
          wmostr="IUTN06"
    elif ( -35.0 <= clat < 50.0 and 180.0 <= clon < 220.0 ):
          wmostr="IUTN07"
    elif ( -35.0 <= clat < 50.0 and 130.0 <= clon < 180.0 ):
          wmostr="IUTN08"
    elif ( 42.0 <= clat <= 75.0 and 232.0 <= clon < 251.0 ):
          wmostr="IUTN06"
    elif ( 42.0 <= clat < 52.0 and 220.0 <= clon < 232.0 ):
          wmostr="IUTN06"
    elif ( -35.0 <= clat < 50.0 and 180.0 <= clon < 220.0 ):
          wmostr="IUTN07"
    elif ( -35.0 <= clat < 50.0 and 130.0 <= clon < 180.0 ):
          wmostr="IUTN08"
    elif ( 52.0 <= clat <= 75.0 and 220.0 <= clon < 232.0 ):
          wmostr="IUTN09"
    elif ( 50.0 <= clat <= 75.0 and 130.0 <= clon < 220.0 ):
          wmostr="IUTN09"
    else:
          wmostr="IUTN06"

    return wmostr

##############################################################3

def fix_nucaps_file(filepath):

    newfilepath = filepath+".tmp"
    copy(filepath, newfilepath)

    try:
       h5_fh = h5py.File(newfilepath, "a")
    except IOError:
       print ('Error opening: {}'.format(newfilepath))
       raise SystemExit
    except OSError:
       print ('Error accessing: {}'.format(newfilepath))
       raise SystemExit

    #Change attribute string: time_coverage_end
    attr_value = h5_fh.attrs['time_coverage_start']
    #print ("time cvg = {}".format(attr_value))
    attr_new = attr_value[0:19]+"Z"
    dom = attr_value[8:10]
    hr = attr_value[11:13]
    mn = attr_value[14:16]
    sec = attr_value[17:19]
    h5_fh.attrs['time_coverage_start'] = attr_new

    #determine the center lat/lon to assign a WMO header
    lats = h5_fh['Latitude'].value
    lons = h5_fh['Longitude'].value
    minlat = np.min(lats)
    maxlat = np.max(lats)
    minlon = np.min(lons)
    maxlon = np.max(lons)
    #print ("MxMn lat = {}/{} MxMn lon = {}/{}".format(minlat, maxlat, minlon, maxlon))
    clat=(minlat + maxlat)/2
    clon=(minlon + maxlon)/2
    if clon < 0.0:
       clon=clon+360
    #print ('Center lat/lon in 360 framework: {}/{}'.format(clat,clon))

    #Change attribute string: time_coverage_end
    attr_value = h5_fh.attrs['time_coverage_end']
    attr_new = attr_value[0:19]+"Z"
    h5_fh.attrs['time_coverage_end'] = attr_new

    #Change attribute string: time_coverage_end
    h5_fh.attrs['satellite_name'] = h5_fh.attrs['platform_name']
    del h5_fh.attrs["platform_name"]

    #Rename variable: Latitude
    h5_fh["Latitude@NUCAPS_EDR"] = h5_fh["Latitude"]
    del h5_fh["Latitude"]
    #Rename variable: Longitude
    h5_fh["Longitude@NUCAPS_EDR"] = h5_fh["Longitude"]
    del h5_fh["Longitude"]
    #Rename variable: Skin_Temperature
    h5_fh["Skin_Temperature@NUCAPS_EDR"] = h5_fh["Skin_Temperature"]
    del h5_fh["Skin_Temperature"]
    #Rename variable: Surface_Pressure
    h5_fh["Surface_Pressure@NUCAPS_EDR"] = h5_fh["Surface_Pressure"]
    del h5_fh["Surface_Pressure"]
    #Rename variable: Topography
    h5_fh["Topography@NUCAPS_EDR"] = h5_fh["Topography"]
    del h5_fh["Topography"]
    #Rename variable: View_Angle
    h5_fh["View_Angle@NUCAPS_EDR"] = h5_fh["View_Angle"]
    del h5_fh["View_Angle"]
    #Rename variable: Effective_Pressure
    h5_fh["Effective_Pressure@NUCAPS_EDR"] = h5_fh["Effective_Pressure"]
    del h5_fh["Effective_Pressure"]
    #Rename variable: H2O_MR
    h5_fh["H2O_MR@NUCAPS_EDR"] = h5_fh["H2O_MR"]
    del h5_fh["H2O_MR"]
    #Rename variable: Liquid_H2O_MR
    h5_fh["Liquid_H2O_MR@NUCAPS_EDR"] = h5_fh["Liquid_H2O_MR"]
    del h5_fh["Liquid_H2O_MR"]
    #Rename variable: O3_MR
    h5_fh["O3_MR@NUCAPS_EDR"] = h5_fh["O3_MR"]
    del h5_fh["O3_MR"]
    #Rename variable: Pressure
    h5_fh["Pressure@NUCAPS_EDR"] = h5_fh["Pressure"]
    del h5_fh["Pressure"]
    #Rename variable: SO2_MR
    h5_fh["SO2_MR@NUCAPS_EDR"] = h5_fh["SO2_MR"]
    del h5_fh["SO2_MR"]
    #Rename variable: Temperature
    h5_fh["Temperature@NUCAPS_EDR"] = h5_fh["Temperature"]
    del h5_fh["Temperature"]
    #Rename variable: Stability
    h5_fh["Stability@NUCAPS_EDR"] = h5_fh["Stability"]
    del h5_fh["Stability"]
    #Rename variable: Ascending_Descending
    h5_fh["Ascending_Descending@NUCAPS_EDR"] = h5_fh["Ascending_Descending"]
    del h5_fh["Ascending_Descending"]
    #Rename variable Ice_Liquid_Flag
    h5_fh["Ice_Liquid_Flag@NUCAPS_EDR"] = h5_fh["Ice_Liquid_Flag"]
    del h5_fh["Ice_Liquid_Flag"]
    #Rename variable: Time
    h5_fh["Time@NUCAPS_EDR"] = h5_fh["Time"]
    del h5_fh["Time"]
    #Rename variable: CrIS_FORs
    h5_fh["CrIS_FORs@NUCAPS_EDR"] = h5_fh["CrIS_FORs"]
    del h5_fh["CrIS_FORs"]
    #Rename variable: Quality_Flag
    h5_fh["Quality_Flag@NUCAPS_EDR"] = h5_fh["Quality_Flag"]
    del h5_fh["Quality_Flag"]

    h5_fh.close()
    #
    # this section extracts the valid time from the filename
    # it will need revision if the name changes 
    #ddhhmm = "{}{}{}".format(dom,hr,mn)
    #header="\r\r\n830 \r\r\nIUTN06 KNES "+ddhhmm+"\r\r\n"
    #ddhhmmss = "{}{}{}{}".format(dom,hr,mn,sec)
    #minnum = int(int(mn)/10)
    #wmoidx = "{}{}".format(minnum,sec)
    #ddhhmm = "{}{}{}".format(dom,hr,mn)
    wmoblock = wmo_header_block(clat,clon)
    minnum = int(int(mn)/10)
    wmoidx = "{}{}".format(minnum,sec)
    ddhhmm = "{}{}{}".format(dom,hr,mn)
    #header="\r\r\n830 \r\r\nIUTN06 KNES {}\r\r\n".format(ddhhmmss)
    header="\r\r\n{} \r\r\n{} KNES {}\r\r\n".format(wmoidx,wmoblock,ddhhmm)

    #headerName = "IUTN06_KNES_{}.hdf.{}".format(ddhhmm,wmoidx)
    headerName = "{}_KNES_{}.hdf.{}".format(wmoblock,ddhhmm,wmoidx)
    #print ("Header = {}".format(headerName))
    with open(headerName, 'wb') as newfh:
        newfh.write(b'\x01')
        newfh.write(header)
        with open(newfilepath,'rb') as prevfh:
           copyfileobj(prevfh, newfh)
           prevfh.close()
        newfh.close()
        os.remove(newfilepath)
        #print ('awipsfile = ',headerName)
        return headerName

##############################################################3

def main():
    """Call to run script."""
    args = _process_command_line()
    #
    if not os.path.exists(args.filepath):
        print ('File not found: {}'.format(args.filepath))
        raise SystemExit
   
    #newfilepath = '{}.mod'.format(args.filepath) 
    #copy(args.filepath, newfilepath)
    filepath = args.filepath
    newfile= fix_nucaps_file(filepath)
    print (newfile)
    return


if __name__ == '__main__':
    # this is only executed if the script is run from the command line
    main()
