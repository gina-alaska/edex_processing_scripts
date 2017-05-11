#!/usr/bin/env /awips2/python/bin/python

import urllib, urlparse
import datetime
import sys
import argparse
from time import strftime
from HTMLParser import HTMLParser
from datetime import datetime, timedelta
from pytz import timezone

##############################################################
class MyHTMLParser(HTMLParser):
   def __init__(self):
      HTMLParser.__init__(self)
      self.satfile = []
      self.sattime = []
      self.satsite = []
      self.record = False
      self.fcnt = 0
      self.dtype = dataset
   def handle_starttag(self, tag, attrs):
      """ look for start tag and turn on recording """
      if tag == 'a':
         #print "Encountered a url tag:", tag
         self.record = True 
      #print "Encountered a start tag:", tag
   def handle_endtag(self, tag):
      """ look for end tag and turn on recording """
      if tag == 'a':
         #print "Encountered end of url tag :", tag
         self.record = False 
   def handle_data(self, data):
      """ handle data string between tags """
      if verbose:
         print "Found data line: ", data
      lines = data.splitlines()
      for dline in lines:
         #print "LINE: ",dline
         seg=dline.split('_')
         nsegs = len(seg)
         if nsegs > 2 and seg[1] == 'AWIPS':
            # VIIRS
            if self.dtype == "viirs":
	       if "crefl" in seg[5]:
                  #print "++++ VIIRS crefl ++++"
                  idx = 7
	       elif "dnb" in seg[5]:
                  #print "++++ VIIRS DNB ++++"
                  idx = 7
               else:
                  #print "++++ VIIRS ++++"
                  idx = 6

            # MODIS
            elif self.dtype == "modis":
	       if "crefl" in seg[5]:
                  #print "++++ MODIS crefl ++++"
                  idx = 8
               else:
                  #print "++++ MODIS ++++"
                  idx = 6
            # METOP
            elif self.dtype == "metop":
               #print "++++ METOP ++++"
               idx = 7
            # AVHRR
            elif self.dtype == "avhrr":
               #print "++++ AVHRR ++++"
               idx = 7
               seg[idx] = "20"+seg[idx]
            else:
               print "++++ UNKNOWN ++++"
               continue
            #
            #print "Seg={} Date: {}".format(idx,seg[idx])
            yr = int(seg[idx][0:4])
            mo = int(seg[idx][4:6])
            da = int(seg[idx][6:8])
            hr = int(seg[idx+1][0:2])
            mn = int(seg[idx+1][2:4])
            try:
               ftime = datetime(yr, mo, da, hr, mn)
               #datetime.strptime(ddttstr, "%Y%m%d_%H%M")
            except ValueError:
               print "Invalid date format: {}".format(self.dtype)
               print "Date vars: {}/{}/{} {}:{}".format(mo,da,yr,hr,mn)
               continue

            self.satfile.append(dline)
            fsecs = ftime.strftime("%s")
            self.sattime.append(fsecs)
            # find the source
            if "gilmore" in dline:
               self.satsite.append("gilmore")
            elif "uafgina" in dline:
               self.satsite.append("uafgina")
            elif "barrow" in dline:
               self.satsite.append("barrow")
            else:
               self.satsite.append("unknown")

            self.fcnt += 1
            if verbose:
               print "stored data URL. ftime: {} secs=()".format(ftime, fsecs)

##################

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dataset', nargs='+', choices=['viirs','modis','metop','avhrr'],
        help='satellite sensors to download'
    )
    parser.add_argument(
        '-bm', '--backmins', type=int, action='store', default=6,
        help='num mins back to consider')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )

    args = parser.parse_args()
    return args

######################################################

def main(): 

   global dataset, verbose
   ##++++++++++++++++  Configuration section +++++++++++++++++++++++## 
   #backmins = 31   # hours back from current time to download
   backmins = 61   # hours back from current time to download
   bgntime = datetime.utcnow() - timedelta(minutes=backmins)
   endtime = datetime.utcnow()
   bgnsecs = bgntime.strftime("%s")
   bgnstr = bgntime.strftime("%Y-%m-%d %H%M UTC")
   endstr = endtime.strftime("%Y-%m-%d %H%M UTC")

   ##++++++++++++++++++  end configuration  ++++++++++++++++++++++++## 
   dset_count = {"modis":0,"viirs":0,"avhrr":0,"metop":0}
   #
   args = _process_command_line()
   verbose = args.verbose
   verbose = True
   print "Dates: ",bgnstr," / ",endstr
   #
   downloads = 0
   for dataset in args.dataset:
      print "Requesting: {}".format(dataset)
      #
      if dataset == 'metop':
         listurl = "http://nrt-prod.gina.alaska.edu/products.txt?satellites[]=metop-b&sensors[]=avhrr&processing_levels[]=awips&start_date={0}&end_date={1}".format(bgnstr, endstr)
      else:
         listurl = "http://nrt-prod.gina.alaska.edu/products.txt?sensors[]={0}&processing_levels[]=awips&start_date={1}&end_date={2}".format(dataset, bgnstr, endstr)
      #
      print "URL=",listurl
      sock = urllib.urlopen (listurl)

      htmlSource = sock.read()
      sock.close()
      print "BEGIN HTML ======================================================="
      print htmlSource
      print "END HTML ========================================================="
      rtnval = len(htmlSource)
      print "HTML String length = {}".format(rtnval)
      # instantiate the parser and feed it the HTML page
      parser = MyHTMLParser()
      parser.feed(htmlSource)

      # now parse the file name and retrieve the recent files 
      cnt = 0
      for fileurl in parser.satfile:
         filesecs = parser.sattime[cnt]
         print "filesecs=%s  bgnsecs=%s" %(filesecs, bgnsecs)
         print "Downlink: {}".format(parser.satsite[cnt]) 
         print "Downloading: {}".format(fileurl)
         split = urlparse.urlsplit(fileurl)
         filename = "./{}".format(split.path.split("/")[-1])
         #print "FILENAME=",filename
         #filename = "./" + split.path.split("/")[-1]
         #print "ORIG FILENAME=",filename
         urllib.urlretrieve(fileurl, filename)
         downloads += 1
         dset_count[dataset] += 1
         cnt += 1

   for dataset in args.dataset:
      print "{} files downloaded={}".format(dataset,dset_count[dataset])
   print "Total files downloaded={}".format(downloads)

if __name__ == '__main__':
    main()

