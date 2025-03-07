#!/bin/bash
##################################
ddtt=`date +%Y%m%d`

(
export PYTHONPATH=/awips2/fxa/bin/src:/awips2/python/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/awips2/python/lib
export TZ=/usr/share/zoneinfo/UTC
readonly PROGNAME=$(basename "$0")
readonly LOCKFILE_DIR=/tmp
readonly LOCK_FD=201
readonly CMDARGS=$@

lock() {
    local prefix=$1
    local fd=${2:-$LOCK_FD}
    local lock_file=$LOCKFILE_DIR/$prefix.lock

    # create lock file
    eval "exec $fd>$lock_file"

    # acquier the lock
    flock -n $fd \
        && return 0 \
        || return 1
}

eexit() {
    local error_str="$@"

    echo $error_str
    exit 1
}

main() {
   #
   echo "+++++ Starting CMORPH2 download - `date` ++++++"
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
   # chg to download directory
   cd /data_store/download
   toolDir='/home/awips/testscripts/cmorph2'
   echo "Running: $toolDir/get_cmorph2.py $CMDARGS"
   $toolDir/get_cmorph2.py $CMDARGS 
   #
   if ls | grep CMORPH2
   then
      echo "scp CMORPH2*.nc edex-test.x.gina.alaska.edu:/data_store/dropbox"
      #scp CMORPH2*.nc awips@edex-test.x.gina.alaska.edu:/data_store/dropbox
      echo "Moving files to AWIPS ingest"
      mv CMORPH2*.nc /data_store/dropbox
   else
      echo "No files downloaded"
   fi
   #
   ddtt=`date +%Y%m%d`
   echo "===== End CMORPH2 download - `date` ======"
}
main
#
) >> /awips2/edex/logs/edex-ingest-cmorph2-$ddtt".log" 2>&1

##
