#!/bin/bash
##################################
# chg to download directory
ddtt=`date +%Y%m%d`
#(
echo "+++++ Starting GINA product download: `date` ++++++"
# CHECK IF EDEX IS UP
edex_ingest_ps=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $15 }'`
if [ -z $edex_ingest_ps ]; then
	echo 'EDEXingest is not running. Exiting... No downloads attempted. '
        exit
else
	edex_ingest_pid=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $2 }'`
	echo 'EDEXingest is running :: pid '$edex_ingest_pid''
fi
#
baseDir="/data_store/download"
ingestDir="/awips2/edex/data/manual"
dataBaseDir="/data_store/manual/regionalsat"

cd $baseDir

yyyymmdd=`ls $dataBaseDir | tail -1`
for daynum in `ls $dataBaseDir/$yyyymmdd`
do
   scp einstein:$dataBaseDir/$yyyymmdd/$daynum/* .
done
#
#mv Alaska* $ingestDir
#
ddtt=`date +%Y%m%d`
echo "===== End GINA product download: `date` ======"
#
#) >> /awips2/edex/logs/edex-ingest-lclregsat-$ddtt".log" 2>&1

#
