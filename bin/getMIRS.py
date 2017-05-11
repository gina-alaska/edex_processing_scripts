#!/usr/bin/env /awips2/python/bin/python

import os,sys
import urllib2, urlparse
import urllib 
import datetime
import gzip
from shutil import copy, move
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
            if verbose:
               print "FILE: {} ".format(dline)
            if seg[0] == 'UAF':
               didx = 7
               if seg[4] == 'mirs':
                  didx = 9
               elif seg[4] == 'rain':
                  didx = 8
               elif seg[4] == 'sea':
                  didx = 8
               elif seg[4] == 'snow':
                  didx = 8
               #
               #
               if verbose:
                  print "Seg={} Date: {}".format(didx,seg[didx])
               yr = int(seg[didx][0:4])
               mo = int(seg[didx][4:6])
               da = int(seg[didx][6:8])
               hr = int(seg[didx+1][0:2])
               mn = int(seg[didx+1][2:4])
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
               if verbose:
                  print "Saved data URL"
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
   ingestDir = "/awips2/edex/data/manual"
   downloadDir = "/data_store/download"
   queue_url = "http://hippy.gina.alaska.edu/distro/processing/mirs_awips/"
   src_url = "http://hippy.gina.alaska.edu/distro/processing/mirs_awips/"
   backmins = 120   # minutes back from current time to download
   ##++++++++++++++++++  end configuration  ++++++++++++++++++++++++##

   reftime = datetime.utcnow() - timedelta(minutes=backmins)
   refsecs = reftime.strftime("%s")

   args = _process_command_line()
   verbose = args.verbose
   #verbose = True
   if verbose:
      print "Reference time: ",reftime
   #
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
   #
   os.chdir(downloadDir)
   # now parse the file name and retrieve the recent files 
   cnt = 0
   dcount = 0
   fcount = 0
   totsize = 0
   for filename in parser.satfile:
      next=False
      sparts=filename.split('_')
      sattime = parser.sattime[cnt]
      tdif = int(sattime) - int(refsecs)
      if verbose:
         print "sattime: {}".format(sattime)
         print "stime={}  rtime={}  diff={}".format(sattime, refsecs, tdif)
      if sattime > refsecs:
         dataurl = "{}{}".format(src_url,filename)
         print "Downloading: %s" %(dataurl)
         fcount += 1
         urllib.urlretrieve(dataurl, filename)

         if os.path.isfile(filename):
            fsize = os.path.getsize(filename)
            dcount += 1
            nameseg = filename.split('.')
            basenm = nameseg[0]
            if verbose:
               print "Basename = {}".format(basenm)
            # use base name to create a new name with "Alaska" prefix and ".nc" extension
            newfilename="Alaska_{}.nc".format(basenm)

            # look for ".gz" in file name to indicate compression is needed
            if ".gz" in filename:
               # open compressed file and read out all the contents
               inF = gzip.GzipFile(filename, 'rb')
               s = inF.read()
               inF.close()
               # now write uncompressed result to the new filename
               outF = file(newfilename, 'wb')
               outF.write(s)
               outF.close()
               # make sure the decompression was successful
               if not os.path.exists(newfilename):
                   print "Decompression failed: {}".format(filename)
                   raise SystemExit
               # redirected compression copies to a new file so old compressed file needs to be removed
               os.remove(filename)
               #
               if verbose:
                  print "File decompressed: {}".format(newfilename)

            elif ".nc" in filename:
               move(filename, newfilename)
            #
            # set the file name to point to the uncompressed name
            filename = newfilename
            #
            # OK, ready to move the file to the ingest directory
            print "Moving {} to {}".format(filename, ingestDir)
            move(filename,ingestDir)
            #
         else:
            fsize = 0
         totsize += fsize
      cnt += 1

   print "Files:  valid = {}   downloaded = {}   Total Size = {}".format(fcount,dcount,totsize)

if __name__ == '__main__':
    main()

