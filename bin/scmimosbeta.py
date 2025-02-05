#!/usr/bin/env /awips2/python/bin/python

import sys
import os 
import numpy as np
from numpy import int16
from scipy import ndimage, misc
from shutil import copy, move
import argparse
import datetime
from time import strftime
from datetime import datetime, timedelta
from pytz import timezone
import netCDF4

################################################################################
##  scmiMosaic.py  - a script for creating mosaic compoites of polar satellite 
##                   data.
##  version: 2.10  - revised to account for format changes with polar2grid 3.0
##           2.00  - revised for python 3 installed in latest AWIPS upgrade 
################################################################################
class filePart(object):
   """ simple class for returning satellite file name information """


   def __init__(self, fname):

      self.chnl = []
      self.tilename = []
      self.ftime = []
      self.fsecs = []
      self.stype = []
      self.fname = fname

   def parse_name(self):
      """ parse the file name for information. """

      # split the filename into parts
      #print "fname={}".format(self.fname)
      fparts=self.fname.split('_')
      fplen = len(fparts)
      idx = 0
      # check if file has prefix. If so, add one to the position index 
      if fparts[0] == "AKPOLAR":
         idx = 1
      # Now break down the filename pieces for file info 
      # This is for SNPP VIIRS 
      if "viirs" in self.fname:
         # first check for clavr-x products
         if "_cloud_" in self.fname:
            self.parse_clavrx(fparts)
         elif "_cld_" in self.fname:
            self.parse_clavrx(fparts)
         else:
            self.parse_viirs(fparts)
      # This section is for AQUA & TERRA MODIS
      elif "modis" in self.fname:
         self.parse_modis(fparts)
      # This section is for metob-b avhrr
      elif "avhrr" in self.fname:
         self.parse_avhrr(fparts)
      # This section is for metob-b avhrr
      elif "mosaic" in self.fname:
         self.parse_mosaic(fparts)
      elif "atms" in self.fname:
         self.parse_MIRS(fparts,"atms")
      elif "amsua-mhs" in self.fname:
         self.parse_MIRS(fparts,"amsu")
      elif "amsu-mhs" in self.fname:
         self.parse_MIRS(fparts,"amsu")
      elif "amsr2" in self.fname:
         self.parse_GAASP(fparts,"amsr2")
      else:
         self.unknown_error()
      # This is for MOSAICS
      #elif fparts[idx+6] == "mosaic":
      #   self.parse_mosaic(fparts, fplen, idx)
      # This is for MOSAIC Delta
      #elif fparts[idx+6] == "mosaicdelta":
      #   self.parse_mosaicdelta(fparts, fplen, idx)
      # Anything else is assumed to be MODIS
      #else:
      #   self.parse_modis(fparts, fplen, idx)
         
   def parse_viirs(self, fparts):
      """ parse the viirs file name for information. """
      viirs_dict = {'i01':'.64','i02':'.86','i03':'1.6','i04':'3.7','i05':'11',
            'm03':'.49','m04':'.56','m05':'.67','m09':'1.4','m11':'2.2','m13':'4.0',
            'm14':'8.6','m15':'10.8','m16':'12','dnb':'dnb','sst':'sst'}
      #
      self.stype = "viirs"
      ndx = fparts.index("Polar")
      if ndx >= 3:
         self.tilename = fparts[ndx+1]
         try:
            self.chnl = viirs_dict[fparts[ndx-1]]
         except:
            self.chnl = '0'
         self.dstr = '{}{}00'.format(fparts[ndx+2],fparts[ndx+3][0:4])
      else:
         self.chnl = '0'
         self.stype = 'unknown'
         print("Searching VIIRS: idx={}".format(idx))
         self.unknown_error()

   def parse_clavrx(self, fparts):
      """ parse the clavr-x file name for information. """
      clavrx_dict = {'height':'cldhgt','temp':'cldtemp','base':'cldbase','type':'cldtype','phase':'cldphase',
            'rain':'rain','emiss':'cldemiss','cloud':'cloud'}
      #
      self.stype = "clavrx"
      ndx = fparts.index("Polar")
      if ndx >= 3:
         self.tilename = fparts[ndx+1]
         try:
            self.chnl = clavrx_dict[fparts[ndx-2]]
         except:
            self.chnl = '0'
         if self.chnl == 'cloud':
            self.chnl = clavrx_dict[fparts[ndx-1]]
         self.dstr = '{}{}00'.format(fparts[ndx+2],fparts[ndx+3][0:4])
      else:
         self.chnl = '0'
         self.stype = 'unknown'
         print("Searching CLAVRX: ndx={}".format(ndx))
         self.unknown_error()

   def parse_MIRS(self, fparts, sattype):
      """ parse the file name for microwave product information. """
      micro_dict = {'tpw':'tpw','rate':'rainrate','clw':'clw','swe':'swe','ice':'seaice',
             'sfr':'sfr','cover':'snowcover','183h1':'bt183h','23v':'bt23v'}
      #
      self.stype = sattype
      ndx = fparts.index("Polar")
      if ndx >= 3:
         self.tilename = fparts[ndx+1]
         try:
            self.chnl = micro_dict[fparts[ndx-1]]
         except:
            self.chnl = '0'
         self.dstr = '{}{}00'.format(fparts[ndx+2],fparts[ndx+3][0:4])
      else:
         self.chnl = '0'
         self.stype = 'unknown'
         print("Searching MIRS: idx={}".format(idx))
         self.unknown_error()

   def parse_GAASP(self, fparts, sattype):
      """ parse the file name for microwave product information. """
      gaasp_dict = {'tpw':'tpw','rate':'rainrate','clw':'clw','swe':'swe','ice':'seaice',
             'sfr':'sfr','cover':'snowcover','183h1':'bt183h','23v':'bt23v'}
      #
      self.stype = sattype
      ndx = fparts.index("Polar")
      if ndx >= 3:
         self.tilename = fparts[ndx+1]
         try:
            self.chnl = gaasp_dict[fparts[ndx-1]]
         except:
            self.chnl = '0'
         self.dstr = '{}{}00'.format(fparts[ndx+2],fparts[ndx+3][0:4])
      else:
         self.chnl = '0'
         self.stype = 'unknown'
         print("Searching GAASP: idx={}".format(idx))
         self.unknown_error()

   def parse_modis(self, fparts):
      """ parse the modis file name for information. """
      modis_dict = {'vis01':'.64','vis02':'.86','vis03':'.47','vis04':'.56',
                 'vis06':'1.6','vis07':'2.2','vis13':'.67','bt20':'3.7','bt23':'4.0',
                 'bt27':'6.7','bt28':'7.3','bt29':'8.6','bt30':'9.7','bt31':'11','bt32':'12',
		 'sst':'sst'}
      #
      self.stype = "modis"
      ndx = fparts.index("Polar")
      if ndx >= 3:
         self.tilename = fparts[ndx+1]
         try:
            self.chnl = modis_dict[fparts[ndx-1]]
         except:
            self.chnl = '0'
         self.dstr = '{}{}00'.format(fparts[ndx+2],fparts[ndx+3][0:4])
      else:
         self.chnl = '0'
         self.stype = 'unknown'
         print("Searching MODIS: idx={}".format(idx))
         self.unknown_error()

   def parse_avhrr(self, fparts):
      """ parse the avhrr file name for information. """
      metop_dict = {'band1':'.64','band2':'.86','band3a':'1.6','band3b':'3.7',
            'band4':'11','band5':'12','sst':'sst'}
      self.stype = "avhrr"
      ndx = fparts.index("Polar")
      if ndx >= 3:
         self.tilename = fparts[ndx+1]
         try:
            self.chnl = metop_dict[fparts[ndx-2]]
         except:
            self.chnl = '0'
         self.dstr = '{}{}00'.format(fparts[ndx+2],fparts[ndx+3][0:4])
      else:
         self.chnl = '0'
         self.stype = 'unknown'
         print("Searching AVHRR: idx={}".format(idx))
         self.unknown_error()

   def parse_mosaic(self, fparts):
      """ parse the mosaic file name for information. """
      #
      ndx = fparts.index("Polar")
      if ndx >= 3:
         if fparts[ndx-2] == 'mosaicdelta':
            self.stype = "mosaicdelta"
         else:
            self.stype = "mosaic"
         self.tilename = fparts[ndx+1]
         self.chnl = fparts[ndx-1]
         self.dstr = '{}{}00'.format(fparts[ndx+2],fparts[ndx+3][0:4])
      else:
         self.chnl = '0'
         self.stype = 'unknown'
         print("Searching MOSAIC: idx={}".format(idx))
         self.unknown_error()

   def date_error(self):
         print(self.fname)
         print(self.stype)
         print("Invalid filedate: {}".format(self.fname))
         self.dstr = "199901010000"

   def unknown_error(self):
         print(self.fname)
         print(self.stype)
         print("Unknown file type: {}".format(self.fname))
         self.dstr = "199901010000"
   
   def filesecs(self):
      if len(self.dstr) >= 12:
         yr=int(self.dstr[0:4])
         mo=int(self.dstr[4:6])
         da=int(self.dstr[6:8])
         hr=int(self.dstr[8:10])
         mn=int(self.dstr[10:12])
      else:
         yr=1999
         mo=1
         da=1
         hr=0
         mn=0

      self.ftime = datetime(yr, mo, da, hr, mn)
      self.fsecs = int(self.ftime.strftime("%s"))
      return self.fsecs

   def channel(self):
      return self.chnl

   def tile(self):
      return self.tilename

   def sensor(self):
      return self.stype


#####################################################################

def _process_command_line(bhrs):
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ver 2.10')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )
    parser.add_argument(
        '-po', '--passonly', action='store_true', default=False, 
        help='composite from passes only without previous mosaics'
    )
    parser.add_argument(
        '-i', '--initialize', action='store_true', default=False, 
         help='initialize the composite with only pass data'
    )
    parser.add_argument(
        '-bh', '--backhrs', type=int, action='store', default=bhrs, 
        help='num hrs to read passes')
    args = parser.parse_args()
    return args


#####################################################################
def get_filepaths(basedirectory):
    """ generate the filenames in a directory tree by walking down 
    the tree. """ 
    file_paths = []
    for root, directories, files in os.walk(basedirectory):
        for filename in files:
           # Join the two strings to form the full path
           filepath = os.path.join(root,filename)
           #print "filepath={}".format(filepath)
           file_paths.append(filepath)
           

    return file_paths

#####################################################################
def get_template_path(filepath, sensors, products):
    """ scan all the filenames for files to use as templates for containing  
    the mosaic data. """ 
    # look for  grid
    for sensor in sensors:
       for prod in products:
          if sensor in filepath and prod in filepath:
             if os.path.exists(filepath):
                return (filepath)
          if sensor == "clavrx" and prod in filepath:
             if os.path.exists(filepath):
                return (filepath)

    return ""

#####################################################################
def initAttributes(srcpath):
   """ Initialize the destination netcdf file, change attributes, and 
   return the data array """
   #
   global fillvalue
   #
   try:
      ncfh_src = netCDF4.Dataset(srcpath, "r")
   except IOError:
      print('ERROR. I/O access to read attributes: {}'.format(srcpath))
      return (fillvalue)
   except OSError:
      print('ERROR. System access to read attributes: {}'.format(srcpath))
      return (fillvalue)
   #
   print ("**** Default fillvalue = {}".format(fillvalue))
   dsrc = ncfh_src.variables['data']
   fillvalue = getattr(dsrc, '_FillValue')
   print ("**** New fillvalue = {}".format(fillvalue))
   return (fillvalue)


#####################################################################
def createDestinationFile(destpath, chnlname, dname, dunits, fileddtt, xpos, ypos, destval):
   """ Initialize the destination netcdf file, change attributes, and 
   return the data array """
   #
   global fillvalue
   global scalefactor
   global offset
   global xpixels
   global ypixels
   global mosaicPixelResDict
   #
   try:
      ncfh = netCDF4.Dataset(destpath, mode="w", clobber=True)
      #ncfh.set_auto_scale(False)
   except IOError:
      print('ERROR. Destination I/O access (init): {}'.format(destpath))
      return np.zeros(1) 
   except OSError:
      print('ERROR. Destination System access (init): {}'.format(destpath))
      return np.zeros(1) 
   #
   print("Creating destination file: {}".format(destpath))
   xdim = ncfh.createDimension("x",xpixels)
   ydim = ncfh.createDimension("y",ypixels)
   dset = ncfh.createVariable('data','i2',('x','y'),fill_value=fillvalue)
   xset = ncfh.createVariable('x','i2',('x'))
   yset = ncfh.createVariable('y','i2',('y'))
   projset = ncfh.createVariable('polar_projection','i4')

   (xscale,xoff,yscale,yoff) = mosaicPixelResDict[xpixels] # x & Y scales and offsets
   if xscale == 5000:
      shortname = "polar_alaska_5km"
   elif xscale == 1000:
      shortname = "polar_alaska_1km"
   else:
      shortname = "polar_alaska_{}".format(xscale)
   #
   # write file attributes    
   setattr(ncfh, 'Conventions', "CF-1.7")
   setattr(ncfh, 'creator', "UAF-GINA")
   setattr(ncfh, 'creation_time', fileddtt)
   setattr(ncfh, 'product_tile_height',xpixels)
   setattr(ncfh, 'product_tile_width',xpixels)
   setattr(ncfh, 'number_product_tiles', 80)
   setattr(ncfh, 'pixel_x_size',xscale/1000)
   setattr(ncfh, 'pixel_y_size',xscale/1000)
   setattr(ncfh, 'production_location', 'gina-uaf')
   setattr(ncfh, 'start_date_time', fileddtt)
   setattr(ncfh, 'satellite_id', "MOSAIC")
   setattr(ncfh, 'sector_id', "Polar")
   setattr(ncfh, 'physical_element', chnlname)
   setattr(ncfh, 'product_name', chnlname)
   setattr(ncfh, 'awips_id', "AWIPS_{}".format(chnlname))
   setattr(ncfh, 'product_columns', xpixels * 8)
   setattr(ncfh, 'product_rows', ypixels * 10)
   setattr(ncfh, 'tile_column_offset', xpos)
   setattr(ncfh, 'tile_row_offset', ypos)
   #
   #with np.printoptions(threshold=np.inf):
   #   print (destval)
   setattr(dset, 'coordinates', 'y x')
   setattr(dset, 'units', dunits)
   setattr(dset, 'valid_min', 0)
   setattr(dset, 'valid_max', 32766)
   setattr(dset, 'standard_name', dname)
   setattr(dset, 'grid_mapping', 'polar_projection')
   #showTileSpecs("BEFORE CONVERT", destval, fillvalue,0)
   #destval = np.where(destval > fillvalue, ((destval*scalefactor)+offset), fillvalue)
   destval = np.where(destval > fillvalue, ((destval-offset)/scalefactor), fillvalue)
   destval = destval.astype(int16)
   #showTileSpecs("AFTER CONVERT", destval, fillvalue,0)
   dset[:,:] = destval
   ############### NEWVER #############
   setattr(dset, 'scale_factor', scalefactor)
   setattr(dset, 'add_offset', offset)
   ####################################
   setattr(dset, 'number_product_80', 80)
   #
   setattr(yset, 'units', 'meters')
   setattr(yset, 'standard_name', 'projection_y_coordinate')
   yvals = np.arange(ypos, ypos+ypixels).astype(int16)
   yset[:] = yvals
   setattr(yset, 'scale_factor', yscale)
   setattr(yset, 'add_offset', yoff)
   #
   setattr(xset, 'units', 'meters')
   setattr(xset, 'standard_name', 'projection_x_coordinate')
   xvals = np.arange(xpos, xpos+xpixels).astype(int16)
   xset[:] = xvals
   setattr(xset, 'scale_factor', xscale)
   setattr(xset, 'add_offset', xoff)
   #
   setattr(projset, 'short_name', shortname)
   setattr(projset, 'grid_mapping_name', 'polar_stereographic')
   setattr(projset, 'standard_parallel', 60.)
   setattr(projset, 'straight_vertical_longitude_from_pole', -150.)
   setattr(projset, 'latitude_of_projection_origion', 90.)
   setattr(projset, 'semi_major_axis', 6378137)
   setattr(projset, 'semi_minor_axis', 6356752.31424518)
   setattr(projset, 'false_easting', 0.)
   setattr(projset, 'false_northin', 0.)
   #
   ncfh.close()
   #
   return
#####################################################################
def createTimeDelDestinationFile(destpath, chnlname, fileddtt, xpos, ypos, destval):
   """ Initialize the destination netcdf file, change attributes, and 
   return the data array """
   #
   global fillvalue
   global scalefactor
   global offset
   global xpixels
   global ypixels
   #
   try:
      ncfh = netCDF4.Dataset(destpath, mode="w", clobber=True)
      ncfh.set_auto_scale(False)
   except IOError:
      print('ERROR. Destination I/O access (init): {}'.format(destpath))
      return np.zeros(1) 
   except OSError:
      print('ERROR. Destination System access (init): {}'.format(destpath))
      return np.zeros(1) 
   #
   print("Creating time del destination file: {}".format(destpath))
   elementname = bytes("{} TimeDelta".format(chnlname), encoding="utf-8")
   xdim = ncfh.createDimension("x",xpixels)
   ydim = ncfh.createDimension("y",ypixels)
   dset = ncfh.createVariable('data','i2',('x','y'),fill_value=fillvalue)
   xset = ncfh.createVariable('x','i2',('x'))
   yset = ncfh.createVariable('y','i2',('y'))
   projset = ncfh.createVariable('polar_projection','i4')

   (xscale,xoff,yscale,yoff) = mosaicPixelResDict[xpixels] # x & Y scales and offsets
   if xscale == 5000:
      shortname = "polar_alaska_5km"
   elif xscale == 1000:
      shortname = "polar_alaska_1km"
   else:
      shortname = "polar_alaska_{}".format(xscale)
   # write file attributes    
   setattr(ncfh, 'Conventions', "CF-1.7")
   setattr(ncfh, 'creator', "UAF-GINA")
   setattr(ncfh, 'creation_time', fileddtt)
   setattr(ncfh, 'product_tile_height',xpixels)
   setattr(ncfh, 'product_tile_width',xpixels)
   setattr(ncfh, 'number_product_tiles', 80)
   setattr(ncfh, 'pixel_x_size',xscale/1000)
   setattr(ncfh, 'pixel_y_size',xscale/1000)
   setattr(ncfh, 'production_location', 'gina-uaf')
   setattr(ncfh, 'start_date_time', fileddtt)
   setattr(ncfh, 'satellite_id', "MOSAIC")
   setattr(ncfh, 'sector_id', "Polar")
   setattr(ncfh, 'physical_element', "{} TimeDelta".format(chnlname))
   setattr(ncfh, 'product_name', chnlname)
   setattr(ncfh, 'awips_id', "AWIPS_{}".format(chnlname))
   setattr(ncfh, 'product_columns', xpixels * 8)
   setattr(ncfh, 'product_rows', ypixels * 10)
   setattr(ncfh, 'tile_column_offset', xpos)
   setattr(ncfh, 'tile_row_offset', ypos)
   #
   setattr(dset, 'standard_name', 'time delta')
   setattr(dset, 'coordinates', 'y x')
   setattr(dset, 'units', 'sec')
   setattr(dset, 'valid_min', 0)
   setattr(dset, 'valid_max', 32766)
   setattr(dset, 'grid_mapping', 'polar_projection')
   dset[:,:] = destval
   setattr(dset, 'add_offset', 0)
   setattr(dset, 'scale_factor', 10)
   setattr(dset, 'number_product_80', 80)
   #
   setattr(yset, 'units', 'meters')
   setattr(yset, 'standard_name', 'projection_y_coordinate')
   yvals = np.arange(ypos, ypos+ypixels).astype(int16)
   yset[:] = yvals
   setattr(yset, 'scale_factor', yscale)
   setattr(yset, 'add_offset', yoff)
   #
   setattr(xset, 'units', 'meters')
   setattr(xset, 'standard_name', 'projection_x_coordinate')
   xvals = np.arange(xpos, xpos+xpixels).astype(int16)
   xset[:] = xvals
   setattr(xset, 'scale_factor', xscale)
   setattr(xset, 'add_offset', xoff)
   #
   setattr(projset, 'short_name', shortname)
   setattr(projset, 'grid_mapping_name', 'polar_stereographic')
   setattr(projset, 'standard_parallel', 60.)
   setattr(projset, 'straight_vertical_longitude_from_pole', -150.)
   setattr(projset, 'latitude_of_projection_origion', 90.)
   setattr(projset, 'semi_major_axis', 6378137)
   setattr(projset, 'semi_minor_axis', 6356752.31424518)
   setattr(projset, 'false_easting', 0.)
   setattr(projset, 'false_northin', 0.)
   #
   ncfh.close()

   #
   return

#####################################################################
def readMosaicFile(srcpath, autoScaleFlag):
   """ Read the data section of a previous mosaic """

   global scalefactor
   global offset
   global fillvalue

   if not os.path.exists(srcpath):
      print("ERROR. File to init destination not found: {}".format(destpath))
      return np.zeros(1) 
   try:
      ncfh = netCDF4.Dataset(srcpath, mode="r", clobber=True)
      ncfh.set_auto_scale(autoScaleFlag)
   except IOError:
      print('ERROR. Destination I/O access (init): {}'.format(destpath))
      return np.zeros(1) 
   except OSError:
      print('ERROR. Destination System access (init): {}'.format(destpath))
      return np.zeros(1) 
   #
   dsrc = ncfh.variables['data']
   srcval = dsrc[:,:]
   mosfillval = getattr(dsrc, '_FillValue')
   if mosfillval != fillvalue:
      fillvalue = mosfillvalue
      print ("**** Using prev mosaic fillvalue = {}".format(fillvalue))

   return srcval

#####################################################################
def merge_data(destval, destdelval, srcpath, ageval):
   """ copy the image data from the source file over the image data of
   the destination file""" 
#
   global scalefactor
   global xpixels
   global ypixels
   global offset
   global fillvalue
   global ageLimit
#
   if not os.path.exists(srcpath):
      print("ERROR: Source file to merge not found: {}".format(srcpath))
      return (destval, destdelval)
   try:
      ncfh_src = netCDF4.Dataset(srcpath, "r")
      #ncfh_src.set_auto_scale(False)
   except IOError:
      print('ERROR. I/O access of source to merge: {}'.format(srcpath))
      return (destval, destdelval)
   except OSError:
      print('ERROR. System access of source to merge: {}'.format(srcpath))
      return (destval, destdelval)
   #
   #showTileSpecs("START DEST", destval, fillvalue,0)
   print("Overlaying Data: {}".format(srcpath))
   dsrc = ncfh_src.variables['data']
   srcval = dsrc[:,:]
   srcscale = getattr(dsrc, 'scale_factor')
   srcoff = getattr(dsrc, 'add_offset')
   (xpix,ypix) = srcval.shape
   #showTileSpecs("START SRC", srcval, fillvalue,0)
   testval = np.where((srcval > 65530),fillvalue,srcval)
   #showTileSpecs("TEST SRC", testval, fillvalue,0)
   #############################################
   # convert masked array to ndarray
   srcval = np.ma.getdata(srcval,subok=False)
   
   # now compare the number of pixels in this file and resize if necessary
   ## first check to see if pixel diminsions are off by one
   if (xpixels - xpix) == 1:
      print("==> Tile shape revision. Adding one row")
      newval = np.insert(srcval, 1, srcval[0],axis=0)
      srcval = newval
      (xpix,ypix) = srcval.shape
      #showTileSpecs("ADDED ROW", srcval, fillvalue,0)
   if (ypixels - ypix) == 1:
      print("==> Tile shape revision. Adding one col")
      newval = np.insert(srcval, 1, srcval[:,0],axis=1)
      srcval = newval
      (xpix,ypix) = srcval.shape
      #showTileSpecs("ADDED COL", srcval, fillvalue,0)
   if (xpixels - xpix) == -1:
      print("Tile shape revision. Removing one column")
      srcval = srcval[xpixels-1,:] 
      #showTileSpecs("REMOVE COL", srcval, fillvalue,0)
   if (ypixels - ypix) == -1:
      print("Tile shape revision. Removing one row")
      srcval = srcval[:,ypixels-1] 
      #showTileSpecs("REMOVE ROW", srcval, fillvalue,0)
   (xpix,ypix) = srcval.shape
   srcval = np.where((srcval > 65533),fillvalue,srcval)
   ## now check to see if pixel diminsions are significantly different requiring rescale
   if xpix != xpixels or ypix != ypixels:
      a = float(xpixels)
      b = float(xpix)
      zoomxscale = a / b
      print("********  ZOOMXSCALE = {}".format(zoomxscale))
      print("Grid axis = {}. Rescaling x by factor of {}".format(xpix, zoomxscale))
      a = float(ypixels)
      b = float(ypix)
      zoomyscale = a / b
      print("********  ZOOMYSCALE = {}".format(zoomyscale))
      print("Grid axis = {}. Rescaling y by factor of {}".format(ypix, zoomyscale))
      #newval = ndimage.zoom(srcval, zoomscale, mode='nearest')
      newval = ndimage.zoom(srcval, zoom=(zoomxscale,zoomyscale), mode='nearest')
      srcval = newval
      (xpix,ypix) = srcval.shape
      #showTileSpecs("ZOOMED FINAL", srcval, fillvalue,0)
   ############# NEWVER ###########
   #cvtscale = srcscale / scalefactor
   #cvtoff = (srcoff - offset) / scalefactor
   #srcval = srcval.astype(int16)
   # convert destval to fit destination scale and offset
   #destvalf = destval.astype(float)
   #srcvalf = srcval.astype(float)
   #destvalf = np.where(srcval > fillvalue, (srcvalf*cvtscale)+cvtoff, destvalf)
   #destvalf = np.where(srcval > fillvalue, srcvalf, destvalf)
   ################################
   #showTileSpecs("DEST BEFORE MERGE", destval, fillvalue,0)
   destval = np.where(srcval > fillvalue, srcval, destval)
   #showTileSpecs("MERGED DESTVAL", destval, fillvalue,0)

   #destval = destvalf.astype(int16)
   # now merge in the new time delta values
   # age values are divided by 10 because file is assigned a scale of 10
   #showTileSpecs("AGEVAL", destdelval, fillvalue,0)
   destdelval = destdelval.astype(int16)
   ageval = int(ageval / 10)
   destdelval = np.where(srcval > fillvalue, ageval, destdelval)
   #showTileSpecs("AGED AGEVAL", destdelval, fillvalue,0)
   ##############################################

   # age out older pass data
   maxdelta = ageLimit / 10
   destdelval = np.where(np.logical_and(destdelval > fillvalue, destdelval > maxdelta), fillvalue,  destdelval)
   # remove pass data where pixels were aged out
   destval = np.where(destdelval > fillvalue, destval, fillvalue)
   #showTileSpecs("AGED DESTVAL", destval, fillvalue,0)
   #
   ncfh_src.close()
   return (destval, destdelval)
#####################################################################
def showTileSpecs(idtext,aval,fillval,flag):
    #aval = np.where(aval > fillvalue, aval, 0)
    print("Array is of type: ", type(aval))
    maxaval = aval.max()
    minaval = aval.min()
    apixcnt = np.sum(aval > fillval)
    (px,py) = aval.shape
    print("** {}. MAX={} MIN={} CNT={} SHAPE={}x{}".format(idtext, maxaval, minaval,apixcnt,px,py))
    if flag == 1:
       for x in aval:
          print(x)
    return

#####################################################################
def lastdelta(destpath):
   """ get the most recent time delta in the new mosaic file""" 
   global fillvalue
   #
   if not os.path.exists(destpath):
      print("ERROR. Destination file not found (lastdel): {}".format(destpath))
      return 0 
   try:
      ncfh = netCDF4.Dataset(destpath, "r+", clobber=True)
      ncfh.set_auto_scale(False)
   except IOError:
      print('ERROR. Destination I/O access (lastdel) {}'.format(destpath))
      return 0
   except OSError:
      print('ERROR. Destination System access (lastdel) {}'.format(destpath))
      return 0
   #
   #dset = ncfh.variables['data'][:]
   dset = ncfh.variables['data']
   fillvalue = getattr(dset, '_FillValue')
   delval = dset[:,:]
   ncfh.close()
   #
   pixcnt = np.sum(delval > fillvalue)
   if pixcnt > 0:
      delval = np.where(delval > fillvalue, delval, 32767)
      pixmin = np.min(delval) * 10
   else:
      pixmin = 0
   print ("PIXMIN={}".format(pixmin))
   return pixmin 
   #
#####################################################################

def main():

   ingestDir = "/data_store/dropbox" # source for data to mosaic
   dataStoreSbnDir = "/data_store/sat"  # NWS source for SCMI data to mosaic
   dataStoreManDir = "/data_store/manual/goesr"  # source for data to mosaic

   #######################################################################
   ##################  User Configuration Section ########################
   tmpDir = "/localapps/data/tmp" # temp storage for building mosaic until moved to ingest
   #tmpDir = "/localapps/runtime/satellite/tmp" # tmp directory for building mosaic until moved to ingest
   #tmpDir2 = "/data_store/download" # 2nd choice directory for building mosaic until moved to ingest
   tmpDir2 = "." # 2nd choice directory for building mosaic until moved to ingest
   backhrs = 6             # hours back from current time to check files for composite
   #### NOTE: mosaicDict determines what sensor composites to generate. 
   #          Only uncomment the mosaics that are wanted.
   #    NOTE2: The leading sensor type in the list determines the default scale of the mosaic. 
   #           Best results are with the lowest common resolution
   #  - possible mosaicDict bands: .49,.56,.64,.67,.86,1.4,1.6,2.2,3.7,4.0,6.7,7.3,8.6,9.7,10.8,11,12
   #  - possible mosaicDict products: tpw,swe,clw,rainrate,seaice,snowcover,sst,cldhgt,cldbase 
   #  - possible sensors: viirs, modis, avhrr
   mosaicDict = {         # channel and sensors that are to used for the mosaic
    # "dnb" : ('viirs',),
    #  ".64" : ('viirs','modis','avhrr'),
    # ".86" : ('viirs','modis'),
    # "1.6" : ('viirs','modis'),
    # "3.7" : ('avhrr','modis','viirs'),
    # "6.7" : ('modis',),
    #  "11" : ('avhrr','modis','viirs'),
    #  "12" : ('avhrr','modis','viirs'),
    #  "tpw": ('atms','amsu'),
    #  "swe": ('atms','amsu'),
    # "clw": ('atms','amsu'),
      "rainrate": ('atms','amsu'),
    #  "sfr": ('atms','amsu'),
    #  "seaice": ('atms','amsu'),
    #  "snowcover": ('atms','amsu'),
    #  "sst": ('viirs','modis','avhrr'),
    #  "cldhgt": ('clavrx',),
    # "cldbase": ('clavrx',),
   }
   #
   timeDeltaDict = {     # max time (hrs) for passes used in composites for each channel
      "dnb": 8,
      ".64": 12,
      ".86": 12,
      "1.6": 12,
      "3.7": 24,
      "11": 24,
      "12": 24,
      "tpw":24,
      "swe":24,
      "clw":24,
      "rainrate":8,
      "sfr":8,
      "seaice":24,
      "sst":24,
      "cldhgt":24,
      "cldbase":24,
   }
   #################  End User Configuration Section #####################
   #######################################################################

   mosaicPixelNumDict = {
     2800: ("modis",),
     2300: ("viirs",),
     1400: ("viirs", "modis",),
     1000: ("viirs","clavrx"),
     700 : ("avhrr", "modis","clavrx"),
     140 : ("atms","amsu"),
   }

   global mosaicPixelResDict
   mosaicPixelResDict = {
     2800: (250,-3232391.87024928,-250,418860.86882731),
     2300: (300,-3232351.03561558,-300,418701.32364195),
     1400: (500,-3232529.18369167,-500,418698.331416102),
     1000: (700,-3232223.55583311,-700,418315.142401981),
     700 : (1000,-3232320.13721668,-1000,418080.974107473),
     140 : (5000,-3234602.34800258,-5000,414365.348002585),
   }
   #  this is a dictionary of filename patterns used to search for a 
   #  template to use as a container for building the mosaic. The content
   #  doesn't matter except the data array should be similar
   mosaicDataAttributes = {
     "dnb" : ("equalized_radiance","*1"),   # pixel res 0.7 km
     ".64" : ("toa_bidirectional_reflectance","*1"),   # pixel res 1.0 km
     ".86" : ("toa_bidirectional_reflectance","*1"),   # pixel res 1.0 km
     "1.6" : ("toa_bidirectional_reflectance","*1"),   # pixel res 1.0 km
     "3.7" : ("brightness_temperature", "kelvin"),  # pixel res 1.0 km
     "6.7" : ("brightness_temperature", "kelvin"),  # pixel res 1.0 km
     "11" : ("brightness_temperature", "kelvin"),  # pixel res 1.0 km
     "12" : ("brightness_temperature", "kelvin"),  # pixel res 1.0 km
     "tpw": ("total_precipitable_water","mm"),   # pixel res 5.0 km
     "swe": ("snow_water_equivalence","cm"),   # pixel res 5.0 km
     "clw": ("cloud_liquid_water","mm"),        # pixel res 5.0 km
     "rainrate": ("rain_rate","mm/hr"),   # pixel res 5.0 km
     "sfr": ("snow_fall_rate","mm/hr",),         # pixel res 5.0 km
     "seaice": ("sea_ice","%"),  # pixel res 5.0 km
     "sst": ("sea_surface_skin_temperature","kelvin"),       # pixel res 0.7 km
     "cldhgt": ("height_at_cloud_top","m"),  # pixel res 0.7 km
     "cldbase": ("base_height_of_cloud","m"),  # pixel res 0.7 km
   }
   mosaicLabelDict = {       # element names that are assigned to the mosaic
     "dnb" : "dnb",
     ".64" : ".64 um",
     ".86" : ".86 um",
     "1.6" : "1.6 um",
     "3.7" : "3.7 um",
     "6.7" : "6.7 um",
     "11" :  "11 um",
     "12" : "12 um",
     "tpw": "MIRS TPW Mosaic",
     "swe": "MIRS SWE Mosaic",
     "clw": "MIRS CLW Mosaic",
     "rainrate": "MIRS RainRate Mosaic",
     "sfr": "MIRS SFR Mosaic",
     "seaice": "MIRS Sea Ice Mosaic",
     "sst": "SST",
     "cldhgt": "Cld Top Hgt",
     "cldbase": "Cld Base Hgt",
   }
   # basic tile definitions for the mosaic 
   mosaicTileInitDict = {   # For each file type:  numpixels, scale, offset
     "dnb" : (1000,.0000305,0),
     ".64" : (700,.00213492,1.59754),
     ".86" : (700,.00331741,.011988),
     "1.6" : (700,.00101846,.0468575),
     "3.7" : (700,.00372337,217.358),
     "6.7" : (700,.00250543,206.19),
     "11" : (700,.00335819,208.0),
     "12" : (700,.00335819,208.0),
     "tpw": (140,.00117597,5.2),
     "swe": (140,.000484954,0),
     "clw": (140,.000000701947,0),
     "rainrate": (140,.000839236,0),
     "sfr": (140,.000839236,0),
     "seaice": (140,.00305194,0),
     "sst": (1400,.00073,271),
     "cldhgt": (1000,.6081,75),
     "cldbase": (1000,.6081,75),
   }

   # this list helps to avoid unnecessary processing 
   fileIgnoreList = ["crefl", "viirs_cloud", "viirs_rain", "cld_temp", "cld_reff", 
     "cld_opd", "cld_emiss", "hncc_dnb", "adaptive_dnb", "OT_WCONUS"]

   tileSliceDict = {  # tile name and block position
      "TJ04": (3,5),
   }
   tileSliceDictOrig = {     # tile name and block position
      "TA01": (0,0),
      "TA02": (1,0),
      "TB01": (2,0),
      "TB02": (3,0),
      "TC01": (4,0),
      "TC02": (5,0),
      "TD01": (6,0),
      "TD02": (7,0),
      "TA03": (0,1),
      "TA04": (1,1),
      "TB03": (2,1),
      "TB04": (3,1),
      "TC03": (4,1),
      "TC04": (5,1),
      "TD03": (6,1),
      "TD04": (7,1),
      "TE01": (0,2),
      "TE02": (1,2),
      "TF01": (2,2),
      "TF02": (3,2),
      "TG01": (4,2),
      "TG02": (5,2),
      "TH01": (6,2),
      "TH02": (7,2),
      "TE03": (0,3),
      "TE04": (1,3),
      "TF03": (2,3),
      "TF04": (3,3),
      "TG03": (4,3),
      "TG04": (5,3),
      "TH03": (6,3),
      "TH04": (7,3),
      "TI01": (0,4),
      "TI02": (1,4),
      "TJ01": (2,4),
      "TJ02": (3,4),
      "TK01": (4,4),
      "TK02": (5,4),
      "TL01": (6,4),
      "TL02": (7,4),
      "TI03": (0,5),
      "TI04": (1,5),
      "TJ03": (2,5),
      "TJ04": (3,5),
      "TK03": (4,5),
      "TK04": (5,5),
      "TL03": (6,5),
      "TL04": (7,5),
      "TM01": (0,6),
      "TM02": (1,6),
      "TN01": (2,6),
      "TN02": (3,6),
      "TO01": (4,6),
      "TO02": (5,6),
      "TP01": (6,6),
      "TP02": (7,6),
      "TM03": (0,7),
      "TM04": (1,7),
      "TN03": (2,7),
      "TN04": (3,7),
      "TO03": (4,7),
      "TO04": (5,7),
      "TP03": (6,7),
      "TP04": (7,7),
      "TQ01": (0,8),
      "TQ02": (1,8),
      "TR01": (2,8),
      "TR02": (3,8),
      "TS01": (4,8),
      "TS02": (5,8),
      "TT01": (6,8),
      "TT02": (7,8),
      "TQ03": (0,9),
      "TQ04": (1,9),
      "TR03": (2,9),
      "TR04": (3,9),
      "TS03": (4,9),
      "TS04": (5,9),
      "TT03": (6,9),
      "TT04": (7,9),
   }
   

 #################  End configuration ##############################
   #
   global fillvalue
   global scalefactor
   global offset
   global xpixels
   global ypixels
   global ageLimit
   global gridsize
   #
   args = _process_command_line(backhrs)
   #
   if os.path.isdir(tmpDir):
      print("Tmp directory for building mosaic: {}".format(tmpDir))
   elif os.path.isdir(tmpDir2):
      tmpDir = tmpDir2
      print("Tmp directory for building mosaic: {}".format(tmpDir))
   else:
      tmpDir = "/tmp"
      print("Tmp directory for building mosaic: {}".format(tmpDir))

   agelimit = 12           # default age limit if not specified in timeDeltaDict
   xpixels = 700 
   ypixels = 700 
   gridsize = 1
   #fillvalue = 32767
   fillvalue = -1
   if args.backhrs != backhrs:
      backhrs = args.backhrs
      if args.verbose:
         print("Mosaic time delta redefined: {} hrs".format(args.backhrs))

   curtime  = datetime.utcnow()
   backtime  = datetime.utcnow() - timedelta(hours=backhrs)
   cursecs = int(curtime.strftime("%s"))
   refsecs = int(backtime.strftime("%s"))
   backsecs = int(backtime.strftime("%s"))
   curddtt = curtime.strftime("%Y%m%d_%H%M")
   curfileddtt = curtime.strftime("%Y-%m-%dT%H:%M:%S")
   if args.verbose:
      print('Current time: {0} / secs: {1}'.format(curtime,cursecs))
      print('Mosaic start time - minus {0} hrs: {1} / secs: {2}'.format(
           backhrs,backtime,backsecs))

   passOnlyFlag = False
   if args.passonly == True or args.initialize == True:
      passOnlyFlag = True 
      print("Initialing only with pass data. Ignoring previous mosaics")

   # scan data_store directory for source files
   sbn_paths = []
   man_paths = []
   all_file_paths = []
   currentSubDir = curtime.strftime("%Y%m%d/%H")
   print("Checking current day/hour: {}".format(currentSubDir))
   sbnDirPath = "{}/{}".format(dataStoreSbnDir,currentSubDir)
   manDirPath = "{}/{}".format(dataStoreManDir,currentSubDir)
   sbn_paths = get_filepaths(sbnDirPath)
   man_paths = get_filepaths(manDirPath)
   all_file_paths = all_file_paths + sbn_paths + man_paths
   for i in range(1, backhrs):
      del sbn_paths[:]
      del man_paths[:]
      prevtime  = curtime - timedelta(hours=i)
      prevSubDir = prevtime.strftime("%Y%m%d/%H")
      print("Checking previous day/hour: {}".format(prevSubDir))
      sbnDirPath = "{}/{}".format(dataStoreSbnDir,prevSubDir)
      manDirPath = "{}/{}".format(dataStoreManDir,prevSubDir)
      sbn_paths = get_filepaths(sbnDirPath)
      man_paths = get_filepaths(manDirPath)
      all_file_paths = all_file_paths + sbn_paths + man_paths
   print("Total number of file paths: {}".format(len(all_file_paths)))

   # next step through the dictionary an create mosaics for uncommented fields
   for key, value in mosaicDict.items():
      mosaicSensors = value 
      mosaicChl = key
      templatePath = ""
      # get definitions and attributes for this channel 
      (xpixels,initscale,initoffset) = mosaicTileInitDict[mosaicChl]  # mosaic tile defs 
      (dataname, dataunits) = mosaicDataAttributes[mosaicChl]  # mosaic data attributes
      ypixels = xpixels
      ageLimit = timeDeltaDict[mosaicChl] * 3600  # hrs converted to secs
      print("******************* Mosaic Channel: {} ******************".format(mosaicChl))
      print("*** Sensors: {} Age: {}  pixels: {}".format(mosaicSensors, ageLimit, xpixels)) 
      if args.verbose:
         print('*** Tile defaults xpix: {} scalefactor: {} offset: {}'.format(xpixels, initscale, initoffset)) 
      scalefactor = initscale
      offset = initoffset

      for tileid, (xblk,yblk) in tileSliceDict.items():
         xstart = xblk * xpixels
         ystart = yblk * ypixels 
         print("   ########## Tile ID: {} ##########".format(tileid))
         print("   ### xstart={}  ystart={}".format(tileid, xstart, ystart))
         mosaicPathname="{0}/UAF_AII_UAFGINA_mosaic_{1}_Polar_{2}_{3}.nc".format(
                 tmpDir,mosaicChl,tileid,curddtt)
         mosaicDelPathname="{0}/UAF_AII_UAFGINA_mosaicdelta_{1}_Polar_{2}_{3}.nc".format(
                 tmpDir,mosaicChl,tileid,curddtt)
         if args.verbose:
         	print(("New mosaic tile name: ",mosaicPathname))
         	print(("New mosaic time delta tile name: ",mosaicDelPathname))

         passcnt = 0
         moscnt = 0
         mosdelcnt = 0
         saved_paths = []
         mosaic_paths = []
         mosaicdel_paths = []
         ################################# 
         nowtime  = datetime.utcnow()
         nowddtt = nowtime.strftime("%H:%M:%S")
         print("### Reading file list for {}/{}. Time: {}".format(mosaicChl, tileid, nowddtt))
         ################################# 
         for path in all_file_paths:
            ### skip certain product groups to avoid unneccary processing ####
            for ignorestr in fileIgnoreList:
                if ignorestr in path:
                   #print "Skipping {}".format(path)
                   continue

            # check for zero length files
            if not os.path.exists(path) or os.stat(path).st_size == 0:
               if args.verbose:
                  print("Zero length file: {}".format(path))
               continue

            if tileid in path:

               dirpath,dstorefile = os.path.split(path)
               # anything else should be good for composite
               if "UAF_AII" in dstorefile or "ARH_AII" in dstorefile:
                  thisfile = filePart(dstorefile)
                  fname = thisfile.parse_name()

                  filesecs = thisfile.filesecs()
                  # step through "data_store" pathnames and save the recent ones
                  # separating mosaic paths from single band paths
                  if (thisfile.channel() == mosaicChl and thisfile.tile() == tileid):
                     #print "filesecs={} backsecs={}".format(filesecs, backsecs)
                     #print "sensor={} mosaicsensor={}".format(thisfile.sensor(),mosaicSensors)
                     #print "channel={} tile={}  mosaicchl={}".format(thisfile.channel(),thisfile.tile(), mosaicChl)
                     #print "FOUND: {} filesecs={} timedif={}".format(thisfile.channel(), filesecs, filesecs - backsecs)
                     if filesecs > backsecs: 
                        #if thisfile.sensor() == "mosaic" and passOnlyFlag == False:
                        if thisfile.sensor() == "mosaic":
                           if args.verbose:
                              print("MOSAIC")
                           mosaic_paths.append('{0}.{1}'.format(filesecs,path))
                           moscnt += 1
                        elif thisfile.sensor() == "mosaicdelta":
                           if args.verbose:
                              print("MOSAICDELTA")
                           mosaicdel_paths.append('{0}.{1}'.format(filesecs,path))
                           mosdelcnt += 1
                        elif thisfile.sensor() in mosaicSensors:
                           if args.verbose:
                              print("SENSOR DATA")
                           saved_paths.append('{0}.{1}'.format(filesecs,path))
                           passcnt += 1

         # check if there are passes or a recent mosaic...otherwise skip to next channel
         if passcnt > 0:
            print("Total passes for channel {} and tile {} = {}".format(mosaicChl, tileid, passcnt))
         elif moscnt > 0:
            print("No recent passes but previous mosaic for channel {} and tile {}".format(mosaicChl, tileid))
         else:
            print("No recent passes or mosaics for channel {} and tile {} - skipping".format(mosaicChl, tileid))
            continue

         # sort the directory list 
         saved_paths.sort()
         #
         # Check if there is a previous mosaic and mosaicdelta to copy from 
         prevMosaicPath = ""
         prevMosDelPath = ""
         foundPrevMosFlag = False
         foundPrevMosDelFlag = False
         # This section determines if mosaic files are recent enough to reference
         if moscnt > 0 and passOnlyFlag == False:
            if args.verbose:
               print("Updating from previous Mosaic file..")
            foundPrevMosFlag = True
            mosaic_paths.sort(reverse=True)
            prevMosaicPath = mosaic_paths[0].partition(".")
            refsecs = int(prevMosaicPath[0])
            # look for the time delta mosaic file that matches the time of the mosaic
            if mosdelcnt > 0:
               prevMosDelFile = os.path.basename(prevMosaicPath[2]).replace("mosaic","mosaicdelta")
               for pdpath in mosaicdel_paths:
                  #print "pdpath={}".format(os.path.basename(pdpath))
                     # save the previous timedelta mosaic filename
                  if prevMosDelFile == os.path.basename(pdpath):
                     prevMosDelPath = pdpath.partition(".")
                     print("Updating from previous Time Delta file:\n      {}".format(prevMosDelPath[2]))
                     # Determine the delta time of the most recent mosaic
                     lastTimeDelSecs = lastdelta(prevMosDelPath[2])
                     print("### Timeoffset of last pass is previous file = {}".format(lastTimeDelSecs))
                     refsecs -= lastTimeDelSecs
                     if args.verbose:
                        print("Mosaic refagediff={} ageLimit={}".format((cursecs-refsecs), ageLimit))
                     if (cursecs - refsecs) < ageLimit:
                        foundPrevMosDelFlag = True 
                     else:
                        foundPrevMosFlag = False
                        foundPrevMosDelFlag = False 
                     break

         if args.verbose:
            print("Reference time: {0} diff from cursecs: {1}".format(refsecs,(cursecs - refsecs)))

         # This section checks for recent pass data or reference file 
         if passcnt > 0:
            numlast = len(saved_paths) - 1
            firstPassPath = saved_paths[0].partition(".")
            lastPassPath = saved_paths[numlast].partition(".")
            if int(lastPassPath[0]) >= refsecs: 
               print("Recent passes were detected")
            else:
               print("No passes or mosaics since last composite ... skipping")
               if args.verbose:
                  print("last file: {0} | Reference time: {1}".format(lastPassPath[0],refsecs))
               continue
         elif foundPrevMosFlag == False:
            print("No recent passes and previous mosaic older than age limit... skipping")
            continue

         if args.verbose:
            print("last file: {0} | Reference time: {1}".format(lastPassPath[0],refsecs))

         # If recent previous mosaic files exists read the data arrays
         if foundPrevMosFlag and foundPrevMosDelFlag:
            destval = readMosaicFile(prevMosaicPath[2],True)
            #destval = destval.astype(int16)
            tdeldestval = readMosaicFile(prevMosDelPath[2],False)
            runtimediff = cursecs - int(prevMosDelPath[0])
            tdelsecs = int(runtimediff / 10)
            print("===> Previous mosaic exists:  tdelsecs={}".format(tdelsecs))
            tdeldestval = np.where((tdeldestval > fillvalue),tdeldestval+tdelsecs,tdeldestval)
         # Otherwise start from scratch
         else:
            print("===> No previous mosaic: Time reset to zero") 
            destval = np.zeros((xpixels,ypixels))
            #destval = destval.astype(int16)
            destval.fill(fillvalue)
            tdeldestval = np.zeros((xpixels,ypixels))
            tdeldestval = tdeldestval.astype(int16)
            tdeldestval.fill(fillvalue)

         ## Now step through the list of more recent single band data
         ## and lay each successive pass over the earlier one
         if passcnt > 0:
            initFlag = 1
            for dspath in saved_paths:
               ## read source file attributes 
               lastPassPath = dspath.partition(".")
               thissecs = int(lastPassPath[0])
               if initFlag == 1:
                  fillvalue = initAttributes(lastPassPath[2]) 
                  initFlag = 0
               if args.verbose:
                  print("thissecs={}  diff={}".format(thissecs, (thissecs - refsecs)))
               if thissecs >= refsecs:
                  tdelsecs = cursecs - thissecs
                  #print "MERGING!!!"
                  nowtime  = datetime.utcnow()
                  nowddtt = nowtime.strftime("%H:%M:%S")
                  print("      ###############################################")
                  print("      ### Bgn merge time: {}".format(nowddtt))
                  print("merge_data({},{},{})".format(lastPassPath[2],mosaicPathname, tdelsecs))
                  (destval,tdeldestval) = merge_data(destval,tdeldestval,lastPassPath[2],tdelsecs)
                  print("*****File Data Merged!!!!!!!")
               #
         # lastly check if the tile has any valid data before creating tile file
         if (np.count_nonzero(destval > fillvalue)):
            print("Creating mosaic file: {}".format(mosaicPathname))
            createDestinationFile(mosaicPathname, mosaicLabelDict[mosaicChl], dataname, dataunits, curfileddtt, xstart, ystart, destval)
            createTimeDelDestinationFile(mosaicDelPathname, mosaicLabelDict[mosaicChl], curfileddtt, xstart, ystart, tdeldestval)
            print("Tile File Updated!!!!!!!!!!!!!!!!!!!!!!!")
            #
            print("Moving {} to {}".format(mosaicPathname, ingestDir))
            #copy(mosaicPathname,ingestDir)
            #move(mosaicPathname,ingestDir)
            #######################move(mosaicPathname,ingestDir)
            print("Moving {} to {}".format(mosaicDelPathname, ingestDir))
            #copy(mosaicDelPathname,ingestDir)
            #move(mosaicDelPathname,ingestDir)
            ##########################move(mosaicDelPathname,ingestDir)
         else:
            print("No valid data. Tile skipped!!!!!!!!!!!!!!!!!!!!!!!")

   return  

if __name__ == '__main__':
    # This is only executed if the script is run from the command line.
    main()
