#!/bin/bash
##################################
# chg to download directory
ddtt=`date +%Y%m%d`
(
export PYTHONPATH=/awips2/fxa/bin/src
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/awips2/python/lib
readonly PROGNAME=$(basename "$0")
readonly LOCKFILE_DIR=/tmp
readonly LOCK_FD=202
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
   echo "+++++ Starting GINA product download (ICING): `date` ++++++"
   lock $PROGNAME \
        || eexit "Only one instance of $PROGNAME can run at one time."
   #
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
   ingestDir="/awips2/edex/data/manual"
   toolDir="/home/awips/bin"
   #
   # CHECK IF THIS IS A TEST SCRIPT
   SPATH="$0"
   echo "script path: $0"
   if [[ $SPATH =~ testscripts ]]
   then
      toolDir='/home/awips/testscripts'
      echo "Test script. Tool path set to: $toolDir"
   fi
   #
   cd $ingestDir
   echo "Running: $toolDir/getIcingSat.py $CMDARGS"
   $toolDir/getIcingSat.py $CMDARGS
   #
   echo "Ingest directory:"
   ls $ingestDir
   #
   ddtt=`date +%Y%m%d`
   echo "===== End GINA product download: `date` ======"
}
main
) >> /awips2/edex/logs/edex-ingest-lcltestsat-$ddtt".log" 2>&1
#
