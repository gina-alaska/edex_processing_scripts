#!/usr/bin/env /awips2/python/bin/python

import sys
import os 
import numpy
from numpy import uint8
from numpy import int8
from shutil import copy, move
import argparse
import datetime
from time import strftime
from datetime import datetime, timedelta
from pytz import timezone
from Scientific.IO import NetCDF

################################################################################
##  makeMosaic.py  - a script for creating mosaic compoites of polar satellite 
##                   data.
##  beta version: 0.99
################################################################################
class filePart(object):
   """ simple class for returning satellite file name information """


   def __init__(self, fname):

      self.chnl = []
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
      if fparts[0] == "Alaska":
         idx = 1
      # Need to check for MODIS icing products first because filename delimters
      # are not "_" but rather "." 
      if "AQU.AKFB" in fparts[idx] or "TER.AKFB" in fparts[idx]:
         f2parts=fparts[1].split('.')
         f2plen = len(f2parts)
         self.parse_modis_ice(f2parts, f2plen)
      # Now break down the filename pieces for file info 
      # This section is for AVHRR
      elif fparts[idx+2] == "AVHRR-AK":
         self.parse_avhrr(fparts, fplen, idx)
      # This section is for avhrr sst which is the same format as metop-b avhrr
      elif fparts[idx+2] == "avhrr":
         self.parse_metopb(fparts, fplen, idx)
     # This is for AMSU microwave
      elif fparts[idx+3] == "amsua-mhs":
         self.parse_mirs(fparts, fplen, idx)
      # This is for METOPB
      elif fparts[idx+2] == "metopb":
         self.parse_metopb(fparts, fplen, idx)
     # This is for ATMS microwave
      elif fparts[idx+3] == "atms":
         self.parse_mirs(fparts, fplen, idx)
      # This is for SNPP VIIRS 
      elif fparts[idx+2] == "npp" or fparts[idx+2] == "j01":
         self.parse_viirs(fparts, fplen, idx)
      # This is for GPM 
      elif fparts[idx+3] == "passiveMicrowave":
            self.parse_gpm(fparts, fplen, idx)
      # This is for MOSAICS
      elif fparts[idx+2] == "mosaic":
         self.parse_mosaic(fparts, fplen, idx)
      # This is for MOSAIC Delta
      elif fparts[idx+2] == "mosaicdelta":
         self.parse_mosaicdelta(fparts, fplen, idx)
      # Anything else is assumed to be MODIS
      else:
         self.parse_modis(fparts, fplen, idx)
         
   def parse_modis_ice(self, f2parts, f2plen):
      """ parse the modis icing file name for information. """
      self.stype = "modisice" 
      try:
         self.chnl = f2parts[4]
      except:
         self.chnl = 0
      if f2plen >= 6:
         yr = int(f2parts[2][0:4])
         jday = int(f2parts[2][4:7])
         # convert julian date to month/day
         tmpdate=datetime(yr, 1, 1) + timedelta(jday-1)
         mmdd = int(tmpdate.strftime("%m%d"))
         self.dstr = '{}{}{}'.format(yr,mmdd,f2parts[3][0:4])
      else: 
         print "modisicing: ch={}  idx={}".format(self.chnl, idx)
         self.date_error()

   def parse_avhrr(self, fparts, fplen, idx):
      """ parse the avhrr file name for information. """
      avhrr_dict = {'ch1':'.64','ch2':'.86','ch3a':'1.6','ch3b':'3.7','ch4':'11','ch5':'12',
	   'sst':'sst'}
      self.stype = "avhrr"
      try:
         self.chnl = avhrr_dict[fparts[idx+4]]
      except:
         self.chnl = 0
      if fplen >= 9 + idx:
         self.dstr = '20{}{}'.format(fparts[idx+7],fparts[idx+8][0:4])
      else:
         self.date_error()

   def parse_metopb(self, fparts, fplen, idx):
      """ parse the avhrr file name for information. """
      metop_dict = {'band1':'.64','band2':'.86','band3a':'1.6','band3b':'3.7',
            'band4':'11','band5':'12','sst':'sst'}
      self.stype = "avhrr"
      try:
         self.chnl = metop_dict[fparts[idx+4]]
      except:
         self.chnl = 0
      if fplen >= 9 + idx:
         self.dstr = '{}{}'.format(fparts[idx+7],fparts[idx+8][0:4])
      else:
         self.date_error()

   def parse_gpm(self, fparts, fplen, idx):
      """ parse the avhrr file name for information. """
      gpm_dict = {'rainRate.nc':'gpmrainrate','overpassTime.nc':'rainratetime'}
      self.stype = "gpm"
      try:
         self.chnl = gpm_dict[fparts[idx+5]]
      except:
         self.chnl = 0
      if fplen >= 6 + idx:
         self.dstr = '{}{}'.format(fparts[idx],fparts[idx+1][0:4])

      else:
         self.date_error()

   def parse_viirs(self, fparts, fplen, idx):
      """ parse the viirs file name for information. """
      viirs_dict = {'i01':'.64','i02':'.86','i03':'1.6','i04':'3.7','i05':'11',
            'm03':'.49','m04':'.56','m05':'.67','m09':'1.4','m11':'2.2','m13':'4.0',
            'm14':'8.6','m15':'10.8','m16':'12','sst':'sst'}
      self.stype = "viirs"
      try:
         self.chnl = viirs_dict[fparts[idx+4]]
      except:
         self.chnl = 0
      if fplen >= 8 + idx:
         self.dstr = '{}{}'.format(fparts[idx+6],fparts[idx+7][0:4])
      else:
         self.date_error()

   def parse_mirs(self, fparts, fplen, idx):
      """ parse the viirs file name for information. """
      mirs_dict = {'mirs':'rainrate','rain':'rainrate','tpw':'tpw','sea':'seaice','snow':'snowcover',
	    'clw':'clw','swe':'swe'}
      # differentiate between amsua-mhs and atms
      if fparts[idx+3] == "atms":
         self.stype = "atms"
      else:
         self.stype = "amsu"
 
      # assign single string channel name
      try:
         self.chnl = mirs_dict[fparts[idx+4]]
      except:
         self.chnl = 0
      # index will need to be incremented for compound names
      if self.chnl == 'rainrate':
         idx += 1
         if fparts[idx+3] == "mhs":
            idx += 1
      elif self.chnl == 'seaice':
         idx += 1
      elif self.chnl == 'snowcover':
         idx += 1
      #  extract the date
      if fplen >= 8 + idx:
         self.dstr = '{}{}'.format(fparts[idx+7],fparts[idx+8][0:4])
         #print "chnl={}   dstr={}".format(self.chnl, self.dstr)
      else:
         self.date_error()

   def parse_modis(self, fparts, fplen, idx):
      """ parse the modis file name for information. """
      modis_dict = {'vis01':'.64','vis02':'.86','vis03':'.47','vis04':'.56',
                 'vis06':'1.6','vis07':'2.2','vis13':'.67','bt20':'3.7','bt23':'4.0',
                 'bt27':'6.7','bt28':'7.3','bt29':'8.6','bt30':'9.7','bt31':'11','bt32':'12',
		 'sst':'sst'}
      self.stype = "modis"
      self.stype = fparts[idx+3]
      try:
         self.chnl = modis_dict[fparts[idx+4]]
      except:
         self.chnl = 0
      if fplen >= 8 + idx:
         self.dstr = '{}{}'.format(fparts[idx+6],fparts[idx+7][0:4])
      else:
         self.date_error()

   def parse_mosaic(self, fparts, fplen, idx):
      """ parse the mosaic file name for information. """
      self.stype = "mosaic"
      try:
         self.chnl = fparts[idx+3]
      except:
         self.chnl = 0
      if fplen >= 6 + idx:
         self.dstr = '{}{}'.format(fparts[idx+4],fparts[idx+5][0:4])
      else:
         print "ch={}  idx={}".format(self.chnl, idx)
         self.date_error()

   def parse_mosaicdelta(self, fparts, fplen, idx):
      """ parse the mosaicdelta file name for information. """
      self.stype = "mosaicdelta"
      try:
         self.chnl = fparts[idx+3]
      except:
         self.chnl = 0
      if fplen >= 6 + idx:
         self.dstr = '{}{}'.format(fparts[idx+4],fparts[idx+5][0:4])
      else:
         self.date_error()

   def date_error(self):
         print self.fname
         print self.stype
         print "Invalid filedate: {}".format(self.fname)
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

   def sensor(self):
      return self.stype


#####################################################################

def _process_command_line(bhrs):
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ver 0.96-C')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )
    parser.add_argument(
        '-po', '--passonly', action='store_true', default=False, help='pass compositing flag'
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
           file_paths.append(filepath)

    return file_paths

#####################################################################
def openDestinationFile(destpath, channel):
   """ open the destination netcdf file, change attributes, and 
   return the file handle """
   #
   if not os.path.exists(destpath):
      print "File not found: {}".format(destpath)
      raise SystemExit
   try:
      fh_dest = NetCDF.NetCDFFile(destpath, "a")
   except IOError:
       print 'Error accessing {}'.format(destpath)
       raise SystemExit
   except OSError:
       print 'Error accessing {}'.format(destpath)
       raise SystemExit
   #
   print "Opening file: {}".format(destpath)
   setattr(fh_dest, "satelliteName", "MOSAIC")
   #
   if channel == "ITOP":
      chstr = "Icing Top"
   elif channel == "IBOT":
      chstr = "Icing Base"
   elif channel == "IIND":
      chstr = "Icing Index"
   elif channel == "tpw":
      chstr = "TPW"
   elif channel == "swe":
      chstr = "SWE"
   elif channel == "clw":
      chstr = "CLW"
   elif channel == "rainrate":
      chstr = "rainrate"
   elif channel == "gpmrainrate":
      chstr = "gpmrainrate"
   elif channel == "sst":
      chstr = "SST"
   else:
      chstr = "{0} um".format(channel)

   #
   if "mosaicdelta" in destpath:                  # time delta 
      attstr = "{0} timedelta".format(chstr)
   else:
      attstr = "{0}".format(chstr)
   setattr(fh_dest, "channel", attstr)

   return fh_dest

#####################################################################
def merge_files(fh_dest, srcpath, destpath):
   """ copy the image data from the source file over the image data of
   the destination file""" 
#
   if not os.path.exists(srcpath):
      print "File not found: {}".format(srcpath)
      raise SystemExit
   try:
      fh_src = NetCDF.NetCDFFile(srcpath, "r")
   except IOError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   except OSError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   #
   #
   print "Overlaying: {} onto {}".format(srcpath,destpath)
   vidsrc = fh_src.variables['image']
   viddest = fh_dest.variables['image']

   pixsrc = vidsrc.getValue()
   pixdest = viddest.getValue()
   #
   ########  for Debug   #########
   #pixcnt = numpy.sum(pixsrc != 0)
   #if pixcnt > 0:
   #   print "SOURCE: {} Nonzero pixels".format(pixcnt)
   ###############################
   #
   pixdest = numpy.where(pixsrc != 0, pixsrc, pixdest)
   ########  for Debug   #########
   #pixcnt = numpy.sum(pixdest != 0)
   #if pixcnt > 0:
   #   print "DESTINATION: {} Nonzero pixels".format(pixcnt)
   ###############################
   #
   rtn = viddest.assignValue(pixdest)
   #
   fh_src.close()
#####################################################################
def test_file(srcpath):
   """ copy the image data from the source file over the image data of
   the destination file""" 
#
   if not os.path.exists(srcpath):
      print "File not found: {}".format(srcpath)
      raise SystemExit
   try:
      fh_src = NetCDF.NetCDFFile(srcpath, "r")
   except IOError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   except OSError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   #
   #
   print "TESTING: {}".format(srcpath)
   vidsrc = fh_src.variables['image']
   pixsrc = vidsrc.getValue()
   #
   ########  for Debug   #########
   pixcnt = numpy.sum(pixsrc != 0)
   print "FILE HAS:  {} Nonzero pixels".format(pixcnt)
   #
   fh_src.close()

#####################################################################
def merge_delta_files(fh_dest, srcpath, destpath, ageval):
   """ copy the image data from the source file over the image data of
   the destination file"""
#
   if not os.path.exists(srcpath):
      print "File not found: {}".format(srcpath)
      raise SystemExit
   try:
      fh_src = NetCDF.NetCDFFile(srcpath, "r")
   except IOError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   except OSError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   #
   #
   #print "Adding time of file: {} to destination: {}".format(srcpath,destpath)
   vidsrc = fh_src.variables['image']
   viddest = fh_dest.variables['image']

   pixsrc = vidsrc.getValue()
   pixdest = viddest.getValue()

   pixdest = numpy.where(pixsrc != 0, ageval, pixdest)
   pixdest = pixdest.astype(int8)
   #
   rtn = viddest.assignValue(pixdest)
   #
   fh_src.close()
   #
#####################################################################
def lastdelta(srcpath):
   """ get the most recent time delta in the new mosaic file""" #

   if not os.path.exists(srcpath):
      print "File not found: {}".format(srcpath)
      raise SystemExit
   try:
      fh_src = NetCDF.NetCDFFile(srcpath, "r")
   except IOError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   except OSError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   #
   #
   vidsrc = fh_src.variables['image']
   pixdata = vidsrc.getValue()
   pixcnt = numpy.sum(pixdata != 0)
   if pixcnt > 0:
      pixmin = numpy.min(pixdata[numpy.nonzero(pixdata)])
      delsecs = pixel2timedif(pixmin)
   else:
      delsecs = 0

   return delsecs 
   #
#####################################################################
def update_timedelta(fh_dest, srcpath, destpath, pixdel, pixmax):
   """ update the time delta in the new mosaic file""" #

   if not os.path.exists(srcpath):
      print "File not found: {}".format(srcpath)
      raise SystemExit
   try:
      fh_src = NetCDF.NetCDFFile(srcpath, "a")
   except IOError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   except OSError:
       print 'Error accessing {}'.format(srcpath)
       raise SystemExit
   #
   #
   print "Updating time delta: ",destpath
   vidsrc = fh_src.variables['image']
   viddest = fh_dest.variables['image']
   pixsrc_c = vidsrc.getValue()
   pixsrc = pixsrc_c.astype(uint8)
   #
   pixmax -= pixdel
   #
   pixsrc = numpy.where(pixsrc > pixmax, 0, pixsrc)
   pixsrc = numpy.where(pixsrc != 0, pixsrc + pixdel, pixsrc)
   #
   pixsrc_c = pixsrc.astype(int8)
   rtn = viddest.assignValue(pixsrc_c)
   #
#####################################################################
def dropout_passes(fh_dest, fh_ref):
   """ copy the image data from the source file over the image data of
   the destination file"""
   #
   viddest = fh_dest.variables['image']
   vidref = fh_ref.variables['image']

   pixdest = viddest.getValue()
   pixref = vidref.getValue()

   pixdest = numpy.where(pixref == 0, 0, pixdest)
   #
   rtn = viddest.assignValue(pixdest)
   #
#####################################################################
def timedif2pixel(secdif):
   """ calculate the time difference and convert to pixel value"""
#
   # this scales the time difference in seconds to an unsigned integer
   # using eq: ((difsec-minsec)/maxsec-minsec) * 255
   tdif = float(secdif)  # csec is current time & fsec is file time
   # short version of eq: pixdif = int((tdif/86400.) * 255.)
   pixdif = int(tdif * .002778)
   #print "CONVERT TIME TO HRS  secdif={}  tdif={} pdif={}".format(secdif, tdif, pixdif)
   # make sure pixel values for time differences fall within limits 
   if pixdif > 255:
      pixdif = 255
   if pixdif < 0:
      pixdif = 0
   return pixdif

#####################################################################
def pixel2timedif(pixdif):
   """ convert the pixel value to time delta"""
#
   # this scales the time difference in seconds to an unsigned integer
   # using eq: ((difsec-minsec)/maxsec-minsec) * 255
   # make sure time differences fall within 24 hrs
   if pixdif > 255:
      pixdif = 255
   if pixdif < 0.:
      pixdif = 0.
   #tdif = int(pixdif * 338.82)
   tdif = int(pixdif * 360)
   return tdif

#####################################################################

def main():

   ingestDir = "/awips2/edex/data/manual" # source for data to mosaic
   #ingestDir = "/home/awips/tmp" # source for data to mosaic

   ##################  Configuration section ########################
   dataStoreDir = "/data_store/manual/regionalsat"  # source for data to mosaic
   tmpDir = "/data_store/download" # temp storage for building mosaic until moved to ingest
   #tmpDir = "." # temp storage for building mosaic until moved to ingest
   #tmpDir = "/tmp" # temp storage for building mosaic until moved to ingest
   backhrs = 6             # hours back from current time to check files for composite
   # Possible mosaicDict bands: .49,.56,.64,.67,.86,1.4,1.6,2.2,3.7,4.0,6.7,7.3,8.6,9.7,10.8,11,12
   # Possible mosaicDict products: tpw,swe,clw,rainrate,seaice,snowcover,sst,ITOP,IBOT,IIND 
   # Possible sensors: viirs, modis, avhrr
   mosaicDict = {         # channel and sensors that are to used for the mosaic
    # ".64" : ('viirs','modis','avhrr'),
    # ".86" : ('viirs','modis'),
    # "1.6" : ('viirs','modis'),
    #  "3.7" : ('viirs','modis','avhrr'),
    # "6.7" : ('modis'),
      "11" : ('viirs','modis','avhrr'),
    #  "12" : ('viirs','modis','avhrr'),
      "tpw": ('atms','amsu'),
    #  "swe": ('atms','amsu'),
    #  "clw": ('atms','amsu'),
      "rainrate": ('atms','amsu'),
    #  "seaice": ('atms','amsu'),
    #  "snowcover": ('atms','amsu'),
      "gpmrainrate": ('gpm'),
      "sst": ('viirs','modis','avhrr'),
    #  "ITOP": ('viirsice','modisice'),
    #  "IBOT": ('viirsice','modisice'),
    #  "IIND": ('viirsice','modisice'),
   }
   timeDeltaFlag = 1     # toggle on/off the creation of time/delta flag
   timeDeltaDict = {     # max time (hrs) for passes used in composites for each channel
      ".64": 12,
      ".86": 12,
      "1.6": 12,
      "3.7": 24,
      "11": 24,
      "12": 24,
      "rainrate":12,
      "seaice":24,
      "snowcover":24,
      "tpw":24,
      "swe":24,
      "clw":24,
      "sst":36,
      "gpmrainrate":12,
      "ITOP": 24, 
      "IBOT": 24,
      "IIND": 24,
      }
   #################  End configuration ##############################
   #
   agelimit = 12           # default age limit if not specified in timeDeltaDict
   args = _process_command_line(backhrs)
   if args.backhrs != backhrs:
      backhrs = args.backhrs
      if args.verbose:
         print "Mosaic time delta redefined: {} hrs".format(args.backhrs)

   curtime  = datetime.utcnow()
   backtime  = datetime.utcnow() - timedelta(hours=backhrs)
   cursecs = int(curtime.strftime("%s"))
   refsecs = int(backtime.strftime("%s"))
   backsecs = int(backtime.strftime("%s"))
   curddtt = curtime.strftime("%Y%m%d_%H%M")
   if args.verbose:
      print 'Current time: {0} / secs: {1}'.format(curtime,cursecs)
      print 'Mosaic start time - minus {0} hrs: {1} / secs: {2}'.format(
           backhrs,backtime,backsecs)

   all_file_paths = []
   all_file_paths = get_filepaths(dataStoreDir)

   for key, value in mosaicDict.iteritems():
      mosaicSensor = value 
      mosaicChl = key
      ageLimit = timeDeltaDict[mosaicChl] * 3600  # hrs converted to secs
      print 'Mosaic channel: {} using: {} Max age: {}'.format(mosaicChl, mosaicSensor, ageLimit) 
      cnt = 0
      mcnt = 0
      mdcnt = 0
      saved_paths = []
      mosaic_paths = []
      mosaicdel_paths = []
      for path in all_file_paths:
         # check for zero length files
         if os.stat(path).st_size == 0:
            if args.verbose:
               print "Zero length file: {}".format(path)
            continue
         dirpath,dstorefile = os.path.split(path)
         # anything else should be good for composite
         if "Alaska_UAF" in dstorefile or "AKFB" in dstorefile or "passiveMicrowave" in dstorefile:
            thisfile = filePart(dstorefile)
            fname = thisfile.parse_name()
            filesecs = thisfile.filesecs()
            #print "filesecs={} backsecs={}".format(filesecs, backsecs)
            #print "sensor={} mosaicsensor={}".format(thisfile.sensor(),mosaicSensor)
            #print "channel={} mosaicchl={}".format(thisfile.channel(),mosaicChl)
            # step through "data_store" pathnames and save the recent ones
            # separating mosaic paths from single band paths
            if (thisfile.channel() == mosaicChl):
               #print "FOUND: {} filesecs={} timedif={}".format(thisfile.channel(), filesecs, filesecs - backsecs)
               if filesecs > backsecs: 
                  if thisfile.sensor() == "mosaic" and args.passonly == False:
                     if args.verbose:
                        print "MOSAIC"
                     mosaic_paths.append('{0}.{1}'.format(filesecs,path))
                     mcnt += 1
                  elif thisfile.sensor() == "mosaicdelta":
                     if args.verbose:
                        print "MOSAICDELTA"
                     mosaicdel_paths.append('{0}.{1}'.format(filesecs,path))
                     mdcnt += 1
                  elif thisfile.sensor() in mosaicSensor:
                     if args.verbose:
                        print "SENSOR DATA"
                     saved_paths.append('{0}.{1}'.format(filesecs,path))
                     cnt += 1

      #
      # make sure there are passes to add... otherwise skip to next channel
      if cnt < 1:
         print "No recent passes found for channel {} - skipping".format(mosaicChl)
         continue
      
      # create a name for the new mosaic image file
      mosaicPathname="{0}/Alaska_UAF_AWIPS_mosaic_{1}_{2}.nc".format(
           tmpDir,mosaicChl,curddtt)
      print "New mosaic name: ",mosaicPathname
      if timeDeltaFlag:
	   mosaicDelPathname="{0}/Alaska_UAF_AWIPS_mosaicdelta_{1}_{2}.nc".format(
              tmpDir,mosaicChl,curddtt)
           print "New mosaic time delta name: ",mosaicDelPathname

      # sort the directory list 
      saved_paths.sort()
      #
      # MOSAIC:  check if there is an earlier mosaic file to start with
      # If not, use a single band file (attributes will be changed later) 
      if mcnt > 0:
         mosaic_paths.sort(reverse=True)
         prevMosaicPath = mosaic_paths[0].partition(".")
         if args.verbose:
            print "Updating from previous Mosaic file:\n      {}".format(prevMosaicPath[2])
      else:
         prevMosaicPath = saved_paths[0].partition(".")
         if args.verbose:
            print "Mosaic file not found! Using latest pass:\n      {}".format(prevMosaicPath[2])
      #
      refsecs = int(prevMosaicPath[0])
      #
      # MOSAIC TIME DELTA - start with latest single band file (attributes will be changed later) 
      prevMosDelPath = saved_paths[0].partition(".")
      if args.verbose:
         print "Start with regular file:\n      {}".format(prevMosDelPath[2])
      # Use a the modified mosaic name to check if there is a previous delta file to use  
      # instead. If not found, single band file will remain 
      mosDeltaFile = os.path.basename(prevMosaicPath[2]).replace("mosaic","mosaicdelta")
      # print "SEARCH STRING={}".format(mosDeltaFile)
      if mdcnt > 0:
         for pdpath in mosaicdel_paths:
            #print "pdpath={}".format(os.path.basename(pdpath))
            if mosDeltaFile == os.path.basename(pdpath):
               # save the previous file as the container for the timedelta mosaic
               prevMosDelPath = pdpath.partition(".")
               print "Updating from previous Time Delta file:\n      {}".format(prevMosDelPath[2])
               # determine the delta time of the most recent pass in the last mosaic
               offset = lastdelta(prevMosDelPath[2])
               print "OFFSET={}".format(offset) 
               refsecs -= offset
               break

      if args.verbose:
         print "Reference time: {0} diff from cursecs: {1}".format(refsecs,(cursecs - refsecs))

      # check if there is data more recent than the reference file 
      numlast = len(saved_paths) - 1
      firstPassPath = saved_paths[0].partition(".")
      lastPassPath = saved_paths[numlast].partition(".")
      if args.verbose:
         print "last file: {0} | reference: {1}".format(lastPassPath[0],refsecs)

      # Make a copy of the file selected as the starting container for
      # the mosaic with the new mosaic name 
      if int(lastPassPath[0]) >= refsecs: 
         copy(prevMosaicPath[2],mosaicPathname)
         copy(prevMosDelPath[2],mosaicDelPathname)
      else:
         print "No passes later than last mosaic... skipping"
         continue

      # Open destination file and redefine global attributes
      fh_dest = openDestinationFile(mosaicPathname, mosaicChl)
      if timeDeltaFlag:
         fh_tdeldest = openDestinationFile(mosaicDelPathname, mosaicChl)
 
      # Need to add time age difference to previous mosaic times
      if mdcnt > 0:
         pixtimedel = timedif2pixel(cursecs - int(prevMosDelPath[0]))
         pixtdelmax = timedif2pixel(ageLimit) 
         if args.verbose:
            print "TIMEDELTA={}  MAXDELTA={}".format(pixtimedel, pixtdelmax)
         update_timedelta(fh_tdeldest,prevMosDelPath[2],mosaicDelPathname,pixtimedel,pixtdelmax)

      ## Now step through the list of more recent single band data
      ## and lay each successive pass over the earlier one
      for dspath in saved_paths:
         lastPassPath = dspath.partition(".")
         thissecs = int(lastPassPath[0])
         if args.verbose:
            print "thissecs={}  diff={}".format(thissecs, (thissecs - refsecs))
         if thissecs >= refsecs:
            #print "MERGING!!!"
            merge_files(fh_dest,lastPassPath[2],mosaicPathname)
            if timeDeltaFlag:
               pixtimedel = timedif2pixel(cursecs - thissecs)
               if args.verbose:
                  print "TIMEDELTA={} cursecs={} filesecs={}".format(pixtimedel,cursecs,thissecs)
               merge_delta_files(fh_tdeldest,lastPassPath[2],mosaicDelPathname,pixtimedel)

      #
      #  Remove pass data that exceeds assigned age limit
      if timeDeltaFlag:
         dropout_passes(fh_dest, fh_tdeldest)

      vtmdest = fh_dest.variables['validTime']
      rtn = vtmdest.assignValue(cursecs)
      fh_dest.close()
      #test_file(mosaicPathname)
   
      if timeDeltaFlag:
         vtmdest = fh_tdeldest.variables['validTime']
         rtn = vtmdest.assignValue(cursecs)
         fh_tdeldest.close()

      del saved_paths[:]
      del mosaic_paths[:]

      print "Moving {} to {}".format(mosaicPathname, ingestDir)
      move(mosaicPathname,ingestDir)
      if timeDeltaFlag:
         print "Moving {} to {}".format(mosaicDelPathname, ingestDir)
         move(mosaicDelPathname,ingestDir)

   return   

if __name__ == '__main__':
    # This is only executed if the script is run from the command line.
    main()
