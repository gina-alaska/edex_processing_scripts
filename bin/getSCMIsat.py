#!/usr/bin/env /awips2/python/bin/python

import os
import urllib2, urlparse
import urllib 
import datetime
import argparse
from HTMLParser import HTMLParser
from datetime import datetime, timedelta
from pytz import timezone


class MyHTMLParser(HTMLParser):
   def __init__(self):
      HTMLParser.__init__(self)
      self.dirflag = dirflag
      if self.dirflag:
         self.satdir = []
         self.sattime = []
      self.satfile = []
      self.record = False
      self.verbose = verbose
      self.fcnt = 0
   def handle_starttag(self, tag, attrs):
      if tag == 'a':
         #print "Encountered a url tag:", tag
         self.record = True 
      #print "Encountered a start tag:", tag
   def handle_endtag(self, tag):
      if tag == 'a':
         #print "Encountered end of url tag :", tag
         self.record = False 
   def handle_data(self, data):

      if self.verbose:
         chartext=data.strip()
         if len(chartext) > 1:
            print "Found data line: {}".format(chartext)
      lines = data.splitlines()
      curtime = datetime.utcnow()
      for dline in lines:
         if self.dirflag:
            #print "LINE: {}".format(dline)
            seg = dline.split('.')
            #print "Num segs = {}".format(len(seg))
            if len(seg) > 2:
               product = seg[0]
               datestr = seg[1]
               timestr = seg[2]
               #print "product={} datestr={}  timestr={}".format(product, datestr, timestr)
               #print "product: {} ddtt: {}".format(product, ddtt)
               # test for only requested product group
               #if product == 'NPP':
               if product == 'NPP' or product == 'AQUA' or product == 'TERRA':
                  # if requested set is not found, skip...
                  #print "Seg={} Date: {}".format(idx,seg[idx])
                  yr = int(datestr[0:4])
                  mo = int(datestr[4:6])
                  da = int(datestr[6:8])
                  hr = int(timestr[0:2])
                  mn = int(timestr[2:4])
                  #print "Date vars: {}/{}/{} {}:{}".format(yr,mo,da,hr,mn)
                  try:
                     ftime = datetime(yr, mo, da, hr, mn) 
                  except ValueError:
                     print "Invalid date format: {}".format(self.dtype)
                     print "Date vars: {}/{}/{} {}:{}".format(da,mo,yr,hr,mn)
                     continue
                  self.satdir.append(dline)
                  fsecs = ftime.strftime("%s")
                  #print "Seconds :", fsecs
                  self.sattime.append(fsecs)
                  # 
                  self.fcnt += 1
                  #print "Saved data URL"
                  if self.verbose:
                     print " --- Data ftime: {} secs=()".format(ftime, fsecs)
               elif seg[1] == 'METOP-B':
                  yr = int(seg[0][2:6])
                  jday = int(seg[0][6:9])
                  mo = 1
                  da = 1
                  hr = int(seg[0][9:11])
                  mn = int(seg[0][11:13])
                  #print "Date vars: {}/{} {}:{}".format(yr,jday,hr,mn)
                  try:
                     ftime = datetime(yr, mo, da, hr, mn) + timedelta(days=(jday-1))
                  except ValueError:
                     print "Invalid date format: {}".format(self.dtype)
                     print "Date vars: {}/{}/{} {}:{}".format(da,mo,yr,hr,mn)
                     continue
                  self.satdir.append(dline)
                  fsecs = ftime.strftime("%s")
                  #print "Seconds :", fsecs
                  self.sattime.append(fsecs)
                  # 
                  self.fcnt += 1
                  #print "Saved data URL"
                  if self.verbose:
                     print " --- Data ftime: {} secs=()".format(ftime, fsecs)

         else:
            #print "LINE: {}".format(dline)
            seg = dline.split('_')
            #print "Num segs = {}".format(len(seg))
            if len(seg) > 2:
               source = seg[0]
               if source == 'SSEC' or source == 'UAF':
                  self.satfile.append(dline)


##################

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-bm', '--backmins', type=int, action='store', default=100,
        help='num mins back to consider')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )

    args = parser.parse_args()
    return args

######################################################


def main ():

   global curtime, verbose, dirflag

   ##++++++++++++++++  Configuration section +++++++++++++++++++++++##
   queue_url = 'http://hippy.gina.alaska.edu/distro/processing/test_awips/'
   ##++++++++++++++++++  end configuration  ++++++++++++++++++++++++##

   args = _process_command_line()
   verbose = args.verbose
 
   reftime = datetime.utcnow() - timedelta(minutes=args.backmins)
   refsecs = reftime.strftime("%s")

   if verbose:
      print "Reference time: ",reftime
   #
   #doy_now = datetime.utcnow().timetuple().tm_yday
   #print "DOY=",doy_now
   #
   # instantiate the parser and feed it the HTML page
   totsize = 0
   totcnt = 0
   dirflag = True
   url_list = []
   pathseg = queue_url.split('/')
   #print "pathseg=",pathseg[7],"url=",queue_url
   response = urllib2.urlopen(queue_url)
   htmlSource = response.read()
   response.close()
   if verbose:
      print "+++++++++++++++++"
      print htmlSource
      print "+++++++++++++++++"
   parser = MyHTMLParser()
   parser.feed(htmlSource)

   dirflag = False
   # now parse the file name and retrieve the recent files 
   dcount = 0
   cnt = 0
   for dir_url in parser.satdir:
      next=False
      sattime = parser.sattime[cnt]
      #print "sattime: {}".format(sattime)
      tdif = int(sattime) - int(refsecs)
      #print "stime={}  rtime={}  diff={}".format(sattime, refsecs, tdif)
      if sattime > refsecs:
         this_url = "{}{}".format(queue_url,dir_url)
         url_list.append(this_url)
      cnt += 1

   # so now should have a list of directory urls
   downloads = 0
   for dir_url in url_list:
      print "File directory: %s" %(dir_url)
      # second html retreival to get list of file names 
      response = urllib2.urlopen(dir_url)
      htmlSource = response.read()
      response.close()
      if verbose:
         print "+++++++++++++++++"
         print htmlSource
         print "+++++++++++++++++"
      parser = MyHTMLParser()
      parser.feed(htmlSource)

      for fname in parser.satfile:
         file_url = "{}{}".format(dir_url,fname)
         print "Downloading: %s" %(file_url)
         fname_new = "AKPOLAR_{}".format(fname)
         urllib.urlretrieve(file_url,fname_new)
         downloads += 1
         if os.path.isfile(fname_new):
            fsize = os.path.getsize(fname_new)
            dcount += 1
         else:
            fsize = 0
         totsize += fsize
         totcnt += dcount
         # this restriction might be used for debug purposes
         #if downloads > 50:
         #   raise SystemExit

   print "Files downloaded = {} Total Size = {}".format(totcnt,totsize)

if __name__ == '__main__':
    main()

