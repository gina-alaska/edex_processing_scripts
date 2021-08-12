#!/bin/bash
##################################
# chg to download directory
ddtt=`date +%Y%m%d`
(
export PYTHONPATH=/awips2/fxa/bin/src:/awips2/python/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/awips2/python/lib
export TZ=/usr/share/zoneinfo/UTC
readonly PROGNAME=$(basename "$0")
readonly LOCKFILE_DIR=/tmp
readonly LOCK_FD=205
readonly CMDARGS=$@
#####
lock() {
    local prefix=$1
    local fd=${2:-$LOCK_FD}
    local lock_file=$LOCKFILE_DIR/$prefix.lock

    # create lock file
    eval "exec $fd>$lock_file"

    # acquire the lock
    flock -n $fd \
        && return 0 \
        || return 1
}
#####
eexit() {
    local error_str="$@"
    echo $error_str
    exit 1
}
#####
main() {
   echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
   echo "++++++++++  Starting Mosaic Scripts - `date` ++++++++++++"
   lock $PROGNAME \
        || eexit "Not Started!! Only one instance of $PROGNAME can run at one time."
   #
   #
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
   echo ""
   echo "<<<<<<< Creating new regionasat Mosaics - `date` >>>>>>>>"
   /home/awips/bin/makeMosaic.py 
   echo ""
   echo "<<<<<<< Creating new SCMI Mosaics - `date` >>>>>>>>"
   #/home/awips/bin/scmiMosaic.py 
   timeout 60m /home/awips/bin/scmiMosaic.py 

   #
   echo "=========== End Mosaic creation - `date` =============="
   #
}
main
) >> /awips2/edex/logs/edex-ingest-lclmosaic-$ddtt".log" 2>&1
##
