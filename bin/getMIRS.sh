#!/bin/bash
##################################
# chg to download directory
ddtt=`date +%Y%m%d`
(
export PYTHONPATH=/awips2/fxa/bin/src:/awips2/python/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/awips2/python/lib
export TZ=/usr/share/zoneinfo/UTC
#
datatype="$1"
echo "+++++ Starting MIRS download - `date` ++++++"
# CHECK IF EDEX IS UP
edex_ingest_ps=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $15 }'`
if [ -z $edex_ingest_ps ]; then
	echo 'EDEXingest is not running. Exiting... No mosaics attempted. '
        exit
else
	edex_ingest_pid=`ps aux | grep ingest | grep -v ingestGrib | grep -v ingestDat | awk '{ print $2 }'`
	echo 'EDEXingest is running :: pid '$edex_ingest_pid''
fi
#

/home/awips/bin/getMIRS.py 

#
ddtt=`date +%Y%m%d`
echo "===== End MIRS download - `date` ======"
#
) >> /awips2/edex/logs/edex-ingest-lclregsat-$ddtt".log" 2>&1

##
