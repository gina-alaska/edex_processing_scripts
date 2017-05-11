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
      self.satfile = []
      self.sattime = []
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
      yr = int(curtime.strftime("%Y"))
      mo = int(curtime.strftime("%m"))
      for dline in lines:
         #print "LINE: {}".format(dline)
         seg = dline.split('_')
         #print "Num segs = {}".format(len(seg))
         if len(seg) > 2:
            product = seg[1]
            ddtt = seg[3]
            #print "product: {} ddtt: {}".format(product, ddtt)
            # test for only requested product group
            if seg[1] == 'IUTN06':
               # if requested set is not found, skip...
               #print "Seg={} Date: {}".format(idx,seg[idx])
               da = int(seg[3][0:2])
               hr = int(seg[3][2:4])
               mn = int(seg[3][4:6])
               #print "Date vars: {}/{} {}:{}".format(yr,mo,hr,mn)
               try:
                  ftime = datetime(yr, mo, da, hr, mn) 
               except ValueError:
                  print "Invalid date format: {}".format(self.dtype)
                  print "Date vars: {}/{}/{} {}:{}".format(da,mo,yr,hr,mn)
                  continue

               self.satfile.append(dline)
               fsecs = ftime.strftime("%s")
               #print "Seconds :", fsecs
               self.sattime.append(fsecs)
               # 
               self.fcnt += 1
               #print "Saved data URL"
               if self.verbose:
                  print " --- Data ftime: {} secs=()".format(ftime, fsecs)

##################

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-bm', '--backmins', type=int, action='store', default=6,
        help='num mins back to consider')
    parser.add_argument(
        '-v', '--verbose', action='store_false', help='verbose flag'
    )

    args = parser.parse_args()
    return args

######################################################


def main ():

   global curtime, verbose

   ##++++++++++++++++  Configuration section +++++++++++++++++++++++##
   queue_url = 'http://hippy.gina.alaska.edu/distro/carl/NUCAPS/'
   backmins = 90   # minutes back from current time to download
   reftime = datetime.utcnow() - timedelta(minutes=backmins)
   #doy_now = datetime.utcnow().timetuple().tm_yday
   #print "DOY=",doy_now
   refsecs = reftime.strftime("%s")

   ##++++++++++++++++++  end configuration  ++++++++++++++++++++++++##
   print "Reference time: ",reftime
   #
   args = _process_command_line()
   verbose = args.verbose
   #verbose = True
 
   # instantiate the parser and feed it the HTML page
   #
   totsize = 0
   totcnt = 0

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

   # now parse the file name and retrieve the recent files 
   dcount = 0
   cnt = 0
   for fname in parser.satfile:
      next=False
      sattime = parser.sattime[cnt]
      #print "sattime: {}".format(sattime)
      tdif = int(sattime) - int(refsecs)
      #print "stime={}  rtime={}  diff={}".format(sattime, refsecs, tdif)
      if sattime > refsecs:
         dataurl = "{}/{}".format(queue_url,fname)
         print "Downloading: %s" %(dataurl)
         urllib.urlretrieve(dataurl, fname)
         if os.path.isfile(fname):
            fsize = os.path.getsize(fname)
            dcount += 1
         else:
            fsize = 0
         totsize += fsize
      cnt += 1
      totcnt += dcount

   print "Files downloaded = {} Total Size = {}".format(totcnt,totsize)

if __name__ == '__main__':
    main()

