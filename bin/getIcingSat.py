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

      polar_list = ['TER','AQU']
      goes_list = ['G-15','G-16']
      #if verbose:
      #   chartext=data.strip()
      #   if len(chartext) > 1:
      #      print "Found data line: {}".format(chartext)
      lines = data.splitlines()
      for dline in lines:
         seg = dline.split('.')
         product = seg[0]
         if len(seg) > 2:
            #
            # test for only requested product group
            #print "FILE: {}/ datatype: {}/ product: {}".format(dline, self.dtype, product)
            savepath = 0
            if self.dtype == 'polar':
               if product in polar_list:
                  savepath = 1
            elif self.dtype == 'goes':
               if product in goes_list:
                  savepath = 1
            elif self.dtype == 'all':
               if product in goes_list or product in polar_list:
                  savepath = 1
            #print "SAVEPATH={}".format(savepath)
            # if requested set is not found, skip...
            if not savepath:
               continue 
            #print "Seg={} Date: {}".format(idx,seg[idx])
            didx = 2
            tidx = 3
            yr = int(seg[2][0:4])
            jday = int(seg[2][4:7])
            mo = 1
            da = 1
            hr = int(seg[3][0:2])
            mn = int(seg[3][2:4])
            #print "Date vars: {}/{} {}:{}".format(yr,jday,hr,mn)
            try:
               #print "days :", timedelta(days=(jday-1))
               #ftime = datetime(yr, mo, da, hr, mn)
               #print "ftime :", ftime
               ftime = datetime(yr, mo, da, hr, mn) + timedelta(days=(jday-1))
               dstring = ftime.strftime("%Y%m%d_%H%M")
               #print "Date: {}".format(dstring)
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
            if verbose:
               print " --- Data ftime: {} secs=()".format(ftime, fsecs)

##################

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dataset', nargs='?', choices=['goes','polar','all'], default='all',
        help='satellite Icing products to download'
    )
    parser.add_argument(
        '-bm', '--backmins', type=int, action='store', default=60,
        help='num mins back to consider')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )

    args = parser.parse_args()
    return args

######################################################


def main ():

   global dataset, verbose

   ##++++++++++++++++  Configuration section +++++++++++++++++++++++##
   #queue_paths = ['http://cloudsgate2.larc.nasa.gov/prod/website/icing/alaska/modis/awips2-nc/',
   #             'http://cloudsgate2.larc.nasa.gov/prod/website/icing/alaska/goesw/awips2-nc/']
   queue_paths = ['http://satcorps.larc.nasa.gov/prod/website/icing/alaska/modis/awips2-nc/',
                'http://satcorps.larc.nasa.gov/prod/website/icing/alaska/goesw/awips2-nc/']
   ##++++++++++++++++++  end configuration  ++++++++++++++++++++++++##
   args = _process_command_line()
   verbose = args.verbose

   reftime = datetime.utcnow() - timedelta(minutes=args.backmins)
   refsecs = reftime.strftime("%s")

   dataset = args.dataset
   if verbose:
      print "Reference time: {} dataset: {}".format(reftime,dataset)
   #
 
   # instantiate the parser and feed it the HTML page
   #
   totsize = 0
   totcnt = 0
   for queue_url in queue_paths:
      pathseg = queue_url.split('/')
      print "pathseg=",pathseg[7],"  url=",queue_url
      if pathseg[7] in queue_url:
         response = urllib2.urlopen(queue_url)
         htmlSource = response.read()
         response.close()
         #print "+++++++++++++++++"
         #print htmlSource
         #print "+++++++++++++++++"
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
               fname_new = "Alaska_{}".format(fname)
               print "Downloading: %s" %(dataurl)
               urllib.urlretrieve(dataurl, fname_new)
               if os.path.isfile(fname_new):
                  fsize = os.path.getsize(fname_new)
                  dcount += 1
               else:
                  fsize = 0
               totsize += fsize
            cnt += 1
         totcnt += dcount

   print "Files downloaded = {} Total Size = {}".format(totcnt,totsize)

if __name__ == '__main__':
    main()

