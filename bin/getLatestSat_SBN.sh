#!/bin/bash
##################################
# chg to download directory
baseDir="/data_store/download"
ingestDir="/awips2/edex/data/manual"
cd $baseDir
#
# remove any previously downloaded files
if [ -f sat.last.tar ]
then
   rm sat.last.tar
fi
# get the latest satellite tar file
wget http://collaborate2.nws.noaa.gov/canned_data/data_files/sat.last.tar
# untar the file
tar -xvf sat.last.tar
#
for dir in `du sat | cut -f2`
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
rm sat.last.tar
#
