#!/bin/bash
##################################
# chg to download directory
baseDir="/data_store/download"
ingestDir="/awips2/edex/data/manual"
srcname="$1"
srcfile="$srcname"."last.tar"
#
cd $baseDir
#
# remove any previously downloaded files
if [ -f "$srcfile" ]
then
   rm "$srcfile"
fi
# get the latest satellite tar file
wget http://collaborate2.nws.noaa.gov/canned_data/data_files/$srcfile
# untar the file
tar -xvf $srcfile
#
for dir in `du $srcname | cut -f2`
do
   echo "------------------------------"
   echo "DIR: $dir"
   for filenm in `ls $dir`
   do
      #echo ">> $filenm "
      if [ -f "$dir/$filenm" ]
      then
         echo "mv $dir/$filenm to $ingestDir"
         mv $dir/$filenm $ingestDir
      fi
   done
   echo "rmdir $dir"
   rmdir $dir
done
#
if [ -f "$srcfile" ]
then
   rm "$srcfile"
fi
#
