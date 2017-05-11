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
      self.dtype = dataset
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
      #rgb_list = ['are','arn','arw','alaska']
      rgb_list = ['arn','alaska']
      fogst_list = ['IFRPROB','CPHASE','LIFRPROB','GM05','GM06']
      #ash_list = ['GM01','GM02','GM03','BTD1112','VISREF','IRWBT']
      #ash list minus single channel visible and IR 
      ash_list = ['GM01','GM02','GM03','BTD1112']
      qpe_list = ['qpe000hr.gz','qpe001hr.gz','qpe003hr.gz','qpe006hr.gz','qpe012hr.gz',
                 'sfr.gz','sfr10.gz','sfr18.gz','sfr35.gz']
      if verbose:
         chartext=data.strip()
         if len(chartext) > 1:
            print "Found data line: {}".format(chartext)
      lines = data.splitlines()
      for dline in lines:
         seg = dline.split('_')
         if len(seg) > 2:
            print "FILE: {} / {}".format(dline, dataset)
            if seg[2] == 'sport':
               if 'sport' not in dataset:
                  print " --- Ignoring SPORT products."
                  continue
               if product == 'rgb' and seg[4] not in rgb_list:
                  print " --- Ignoring non-RGB product: {}".format(seg[4])
                  continue
               if product == 'qpe' and seg[5] not in qpe_list:
                  print " --- Ignoring non-QPE product: {}".format(seg[5])
                  continue
               idx = 0
            elif seg[2] == 'GEOCAT-MOD':
               if 'geocat' not in dataset:
                  print " --- Ignoring GEOCAT products."
                  continue
               if product == 'fogst' and seg[5] not in fogst_list:
                  print " --- Ignoring non-FOGST product: {}".format(seg[5])
                  continue
               if product == 'ash' and seg[5] not in ash_list:
                  print " --- Ignoring non-MODIS product: {}".format(seg[5])
                  continue
               idx = 6 
            else:
               print "++++ UNKNOWN PRODUCT ++++"
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
            # 
            self.fcnt += 1
            print "Saved data URL"
            if verbose:
               print " --- Data ftime: {} secs=()".format(ftime, fsecs)

##################

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dataset', nargs='+', choices=['sport','geocat','all'],
        help='satellite CI product to download'
    )
    parser.add_argument(
        '-p', '--product', choices=['rgb','fogst','ash','qpe'],
        default='all', help='product groups to download'
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


def main ():

   global dataset, verbose, product

   ##++++++++++++++++  Configuration section +++++++++++++++++++++++##
   queue_url = "http://ldm.gina.alaska.edu/queue/exp"
   src_url = "http://ldm.gina.alaska.edu/data/ldm/exp"
   backmins = 61   # hours back from current time to download
   reftime = datetime.utcnow() - timedelta(minutes=backmins)
   refsecs = reftime.strftime("%s")

   ##++++++++++++++++++  end configuration  ++++++++++++++++++++++++##
   print "Reference time: ",reftime
   #
   args = _process_command_line()
   verbose = args.verbose
   #verbose = True
   dataset = args.dataset
   if all in dataset:
      dataset.append(sport)
      dataset.append(geocat)
   product = args.product
 
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
         urllib.urlretrieve(dataurl, fname)
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

