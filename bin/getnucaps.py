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
      if verbose:
         chartext=data.strip()
         if len(chartext) > 1:
            print "Found data line: {}".format(chartext)
      lines = data.splitlines()
      for dline in lines:
         seg = dline.split('_')
         if len(seg) > 2:
            print "FILE: {} ".format(dline)
            if seg[0] == 'NUCAPS-EDR':
               #
               #print "Seg={} Date: {}".format(idx,seg[idx])
               yr = int(seg[3][1:5])
               mo = int(seg[3][5:7])
               da = int(seg[3][7:9])
               hr = int(seg[3][9:11])
               mn = int(seg[3][11:13])
               try:
                  ftime = datetime(yr, mo, da, hr, mn)
                  #datetime.strptime(ddttstr, "%Y%m%d_%H%M")
               except ValueError:
                  print "Invalid date format"
                  print "Date vars: {}/{}/{} {}:{}".format(mo,da,yr,hr,mn)
                  continue

               self.satfile.append(dline)
               fsecs = ftime.strftime("%s")
               self.sattime.append(fsecs)
               # 
               self.fcnt += 1
               print "Saved data URL"
               if verbose:
                  print " --- Data ftime: {} secs=()".format(ftime, fsecs)
            else:
               print "++++ UNKNOWN PRODUCT ++++"
               continue


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
        '-v', '--verbose', action='store_true', help='verbose flag'
    )

    args = parser.parse_args()
    return args

######################################################


def main ():

   global verbose

   ##++++++++++++++++  Configuration section +++++++++++++++++++++++##
   queue_url = "http://static.gina.alaska.edu/NPS_products/NUCAPS/direct_readout/"
   src_url = "http://static.gina.alaska.edu/NPS_products/NUCAPS/direct_readout/"
   backmins = 61   # hours back from current time to download
   reftime = datetime.utcnow() - timedelta(minutes=backmins)
   refsecs = reftime.strftime("%s")

   ##++++++++++++++++++  end configuration  ++++++++++++++++++++++++##
   print "Reference time: ",reftime
   #
   args = _process_command_line()
   verbose = args.verbose
   #verbose = True
 
   # instantiate the parser and feed it the HTML page
   #
   response = urllib2.urlopen(queue_url)
   htmlSource = response.read()
   response.close()
   #print "+++++++++++++++++"
   #print htmlSource
   #print "+++++++++++++++++"
   parser = MyHTMLParser()
   parser.feed(htmlSource)

   # now parse the file name and retrieve the recent files 
   cnt = 0
   dcount = 0
   totsize = 0
   for fname in parser.satfile:
      next=False
      sparts=fname.split('_')
      sattime = parser.sattime[cnt]
      #print "sattime: {}".format(sattime)
      tdif = int(sattime) - int(refsecs)
      #print "stime={}  rtime={}  diff={}".format(sattime, refsecs, tdif)
      if sattime > refsecs:
         dataurl = "{}/{}".format(src_url,fname)
         print "Downloading: %s" %(dataurl)
         #urllib.urlretrieve(dataurl, fname)
         if os.path.isfile(fname):
            fsize = os.path.getsize(fname)
            dcount += 1
         else:
            fsize = 0
         totsize += fsize
      cnt += 1

   print "Files downloaded = {} Total Size = {}".format(dcount,totsize)

if __name__ == '__main__':
    main()

