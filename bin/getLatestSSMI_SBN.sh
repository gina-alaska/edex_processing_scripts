#!/bin/bash
##################################
# chg to download directory
baseDir="/data_store/download"
ingestDir="/awips2/edex/data/manual"
cd $baseDir
#
# remove any previously downloaded files
if [ -f bufrssmi.last.tar ]
then
   rm bufrssmi.last.tar
fi
# get the latest satellite tar file
wget http://collaborate2.nws.noaa.gov/canned_data/data_files/bufrssmi.last.tar
# untar the file
tar -xvf bufrssmi.last.tar
#
for dir in `du bufrssmi | cut -f2`
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
   rm bufrssmi.last.tar
#
