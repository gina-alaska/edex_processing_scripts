#!/bin/bash
##################################
# chg to download directory
yymmdd=`date +%Y%m%d`
(
export PYTHONPATH=/awips2/fxa/bin/src
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/awips2/python/lib
#
echo "+++++ Starting GINA product download (NUCAPS): `date` ++++++"
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
testDir="/home/awips/tmp"
cd $ingestDir
#
echo "/home/awips/bin/getNUCAPSsat.py"
/home/awips/bin/getNUCAPSsat.py
#
echo "Ingest directory:"
ls $ingestDir
echo "===== End GINA product download: `date` ======"
) >> /awips2/edex/logs/edex-ingest-lclregsat-$yymmdd".log" 2>&1
#
