#!/bin/bash
##################################
# chg to download directory
ddtt=`date +%Y%m%d`
(
echo "===== Starting Metar download: `date` ======"
# CHECK IF EDEX IS UP
edex_ingest_ps=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $15 }'`
if [ -z $edex_ingest_ps ]; then
	echo ' EDEXingest is not running. Exiting... No downloads attempted. '
        exit
else
	edex_ingest_pid=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $2 }'`
	echo ' EDEXingest is running :: pid '$edex_ingest_pid''
fi
#
baseDir="/data_store/download"
ingestDir="/awips2/edex/data/manual"
cd $baseDir
#
# remove any previously downloaded files
if [ -f metar.last.tar ]
then
   rm metar.last.tar
fi
# get the latest satellite tar file
wget http://collaborate2.nws.noaa.gov/canned_data/data_files/metar.last.tar
# untar the file
tar -xvf metar.last.tar
#
for dir in `du metar | cut -f2`
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
   rm metar.last.tar
#
) >> /awips2/edex/logs/edex-ingest-lclmetar-$ddtt".log" 2>&1

