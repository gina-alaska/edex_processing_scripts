#!/usr/bin/env /awips2/python/bin/python

import urllib.request
import datetime
import os, sys
import gzip
from shutil import copy, move, copyfileobj
import argparse
from time import strftime
#from HTMLParser import HTMLParser
from html.parser import HTMLParser
from datetime import datetime, timedelta
#from pytz import timezone
#import numpy
#import netCDF4
#from nucaps4awips import fix_nucaps_file
#from ncImageQC import qc_image_file

##############################################################
class MyHTMLParser(HTMLParser):
   def __init__(self):
      HTMLParser.__init__(self)
      self.satfile = []
      self.record = False
      self.fcnt = 0
   def handle_starttag(self, tag, attrs):
      """ look for start tag and turn on recording """
      if tag == 'a':
         #print ("Encountered a url tag:", tag)
         self.record = True 
      #print ("Encountered a start tag:", tag)
   def handle_endtag(self, tag):
      """ look for end tag and turn on recording """
      if tag == 'a':
         #print ("Encountered end of url tag :", tag)
         self.record = False 
   def handle_data(self, data):
      """ handle data string between tags """
      if verbose:
         print ("Found data line: ", data)
      lines = data.splitlines()
      for dline in lines:
         #print ("LINE: ",dline)
         # make sure line is not blank
         if len(dline) > 1:
            self.satfile.append(dline)

##################

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'sensor', nargs='+', choices=['viirs','modis','metop','avhrr','atms','amsr2'],
        help='satellite sensors to download'
    )
    parser.add_argument(
        '-a', '--antenna', action='store', default='all', help='antenna source')
    parser.add_argument(
        '-s', '--satellite', action='store', default='all', help='satellite source')
    parser.add_argument(
        '-m', '--match', action='store', default='', help='match substring in filename')
    parser.add_argument(
        '-l', '--level', action='store', default='awips', choices=['awips',
        'mirs_awips','mirs_scmi','scmi','sst_awips','nucaps_level2','clavrx_scmi', 
	'level2','mirs_level2','NucapsAwips'], help='format type')
    parser.add_argument(
        '-t', '--test', action='store_true', help='use test NRT data stream')
    parser.add_argument(
        '-ni', '--noingest', action='store_true', help='no AWIPS ingest, transfer file only')
    parser.add_argument(
        '-reg', '--regionalsat', action='store_true', help='file in old AWIPS format')
    parser.add_argument(
        '-f', '--qcfilter', action='store_true', help='turn on image qc filter')
    parser.add_argument(
        '-bm', '--backmins', type=int, action='store', default=61,
        help='num mins back to consider')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )

    args = parser.parse_args()
    return args

######################################################

def main(): 

   global sensor, verbose, testsrc
   ##++++++++++++++++  Configuration section +++++++++++++++++++++++## 
   ingestDir = "/data_store/dropbox"
   downloadDir = "/data_store/download"
   minPixelCount = 60000    # minimum number of pixels for image to be valid
   minPixelRange = 50       # minimum range of pixel values for valid image
   ##++++++++++++++++++  end configuration  ++++++++++++++++++++++++## 
   #
   ###### definitions base on command line input
   args = _process_command_line()
   verbose = args.verbose      # turns on verbose output
   antenna = args.antenna      # specifies single satellite platform
   satellite = args.satellite  # specifies single satellite platform
   testsrc = args.test         # directs data requests to test NRT stream
   matchstr = args.match       # directs data requests to test NRT stream
   if args.noingest:
      doingest = 0
   else:
      doingest = 1
   #
   if testsrc:
       datasrc = "nrt-test"
   else:
       datasrc = "nrt-prod"
   level = args.level
   #
        
   bgntime = datetime.utcnow() - timedelta(minutes=args.backmins)
   endtime = datetime.utcnow()
   bgnsecs = bgntime.strftime("%s")
   bgnstr = bgntime.strftime("%Y-%m-%d+%H%M")
   endstr = endtime.strftime("%Y-%m-%d+%H%M")
   #print ("format={}  satellite={}".format(level, satellite))
   ######
   dset_count = {"modis":0,"viirs":0,"avhrr":0,"metop":0,"atms":0,"amsr2":0}
   #
   if verbose:
      print ("Dates: ",bgnstr," / ",endstr)
   #
   downloads = 0
   for sensor in args.sensor:
      print ("Requesting: {}".format(sensor))
      #
      if antenna == 'all':          # pull from any antenna source
         if satellite == 'all':     # pull from any satellite source
            listurl = "http://{0}.gina.alaska.edu/products.txt?sensors[]={1}&processing_levels[]={2}&start_date={3}&end_date={4}".format(datasrc, sensor, level, bgnstr, endstr)
         else:                      # specify satellite source from any antenna
            listurl = "http://{0}.gina.alaska.edu/products.txt?satellites[]={1}&sensors[]={2}&processing_levels[]={3}&start_date={4}&end_date={5}".format(datasrc, satellite, sensor, level, bgnstr, endstr)
      #
      else:                         # specify the antenna source
         if satellite == 'all':     # pull from any satellite source
            listurl = "http://{0}.gina.alaska.edu/products.txt?facilities[]={1}&sensors[]={2}&processing_levels[]={3}&start_date={4}&end_date={5}".format(datasrc, antenna, sensor, level, bgnstr, endstr)
         else:                      # specify the antenna and satellite
            listurl = "http://{0}.gina.alaska.edu/products.txt?facilities[]={1}&satellites[]={2}&sensors[]={3}&processing_levels[]={4}&start_date={5}&end_date={6}".format(datasrc, antenna, satellite, sensor, level, bgnstr, endstr)
      #
      print ("URL=",listurl)
      sock = urllib.request.urlopen (listurl)

      htmlSource = str(sock.read(),'UTF-8')
      sock.close()
      if verbose:
         print ("BEGIN HTML =======================================================")
         print (htmlSource)
         print ("END HTML =========================================================")
      rtnval = len(htmlSource)
      print ("HTML String length = {}".format(rtnval))
      # instantiate the parser and feed it the HTML page
      parser = MyHTMLParser()
      parser.feed(htmlSource)

      # change working location to the download scratch directory
      if doingest:
         os.chdir(downloadDir)
      # now parse the file name and retrieve the recent files 
      cnt = 0
      dcount = 0
      ingcount = 0
      totsize = 0
      for fileurl in parser.satfile:
         # the test location for files is different than the operational location
         if testsrc:
            fileurl = fileurl.replace("dds.gina.alaska.edu/nrt","nrt-dds-test.gina.alaska.edu")
         if verbose:
            print ("Downloading: {}".format(fileurl))
         filename = "{}".format(fileurl.split("/")[-1])
         if matchstr:
            #print ("looking for matchstr=[{}]".format(matchstr))
            if matchstr in filename:
               print ("Found: {}".format(filename))
            else:
               continue

         print ("FILENAME={}".format(filename))
         urllib.request.urlretrieve(fileurl, filename)
         if os.path.isfile(filename):
            fsize = os.path.getsize(filename)
            dcount += 1                      
            nameseg = filename.split('.')
            basenm = nameseg[0]              
            if verbose: 
               print ("Basename = {}".format(basenm))
            # use base name to create a new name with "Alaska" prefix and ".nc" extension
            if args.regionalsat:
               newfilename="Alaska_{}.nc".format(basenm)
               print ("Adding prefix: {}".format(newfilename))
            else:
               newfilename=filename

            # now look for ".gz" in file name to determine if compression is needed
            if ".gz" in filename:
               # open compressed file and read out all the contents
               inF = gzip.GzipFile(filename, 'rb')
               s = inF.read()
               inF.close()
               # now write uncompressed result to the new filename
               outF = open(newfilename, 'wb')
               outF.write(s)
               outF.close()
               # make sure the decompression was successful
               if not os.path.exists(newfilename):
                   print ("Decompression failed: {}".format(filename))
                   raise SystemExit
               # redirected compression copies to a new file so old compressed file needs to be removed
               os.remove(filename)
               #
               if verbose:
                  print ("File decompressed: {}".format(newfilename))

            elif ".nc" in filename:
               move(filename, newfilename)
            #
            # set the filename variable to the new uncompressed name
            filename = newfilename
            ###############################################
            # last step is to do QC checks on the data
            if args.qcfilter:
               if qc_image_file(filename, minPixelCount, minPixelRange):
                  print ("Moving {} to {}".format(filename, ingestDir))
                  move(filename,ingestDir)
                  ingcount += 1
               else:
                  print ("QC failed. Removing: {}".format(filename))
                  os.remove(filename)
            ###############################################
            else:
               # Check whether this is nucaps sounding which needs
               # file modification for AWIPS
               if level == 'nucaps_level2':
                   print ("NUCAPS: {}".format(filename))
                   if "NUCAPS-EDR" in filename:
                      origFilename = filename
                      print ("fix nucaps file")
                      filename = fix_nucaps_file(origFilename)
                      print ("new filename = {}".format(filename))
                      if os.path.exists(filename):
                         # a new converted file has been made so remove the original file
                         print ("Removing: {}".format(origFilename))
                         #move(origFilename,"/home/awips/testscripts/testdata")
                         os.remove(origFilename)
                   else:
                      print ("Removing: {}".format(filename))
                      os.remove(filename)
                      continue 
               # Now check if the file already exists ingest directory
               ingestfilename = "{}/{}".format(ingestDir,filename)
               if os.path.exists(ingestfilename):
                  print ("File already exists in Ingest Dir...removing: {}".format(filename))
                  os.remove(filename)
                  continue
               elif doingest:
                  # OK, ready to move the file to the ingest directory
                  print ("Moving {} to {}".format(filename, ingestDir))
                  try:
                     move(filename,ingestDir)
                  except:
                     print ("************  Unable to  move file to ingest: {}".format(filename))
                     continue
               else:
                  print ("No local ingest for {}".format(filename))
               ingcount += 1
               print ("INGEST CNT = {}".format(ingcount))
            #
         else:
            fsize = 0

         totsize += fsize
         downloads += 1
         dset_count[sensor] += 1
         cnt += 1

   for sensor in args.sensor:
      print ("{} files downloaded={}".format(sensor,dset_count[sensor]))
   print ("Total files downloaded={} ingested={}  total size={}".format(downloads, ingcount, totsize))

if __name__ == '__main__':
    main()

