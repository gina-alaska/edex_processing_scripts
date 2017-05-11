#!/bin/bash
##################################
# chg to download directory
ddtt=`date +%Y%m%d`
(
export PYTHONPATH=/awips2/fxa/bin/src
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/awips2/python/lib
#
echo "+++++ Starting GINA product download (ICING): `date` ++++++"
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
cd $baseDir
#
arglist=""
for var in "$@"
do
   if [ "$var" = "goes" ]
   then
      echo "Requesting: $var"
      arglist=$arglist" $var"
   elif [ "$var" = "polar" ]
   then
      echo "Requesting: $var"
      arglist=$arglist" $var"
   else
      echo "Unknown datatype type ($var)!"
   fi
   echo "ARGLIST: $arglist"
done
#
if [ -z "$arglist" ]
then
   echo "No command line arguments. Default is all data types"
   echo ""
   arglist="all"
fi
#
echo "/home/awips/bin/getIcingSat.py $arglist"
/home/awips/bin/getIcingSat.py $arglist
#
#
touch ICING_MARKER
# next unzip and rename the files
for srcname in `ls *.pix.awips2.nc`
do
   if [ "$srcname" = "ICING_MARKER" ]
   then
      rm $srcname
   else
      destname="Alaska_$srcname"
      echo "mv $srcname $destname"
      mv $srcname $ingestDir/$destname
   fi
done
#
rm ICING_MARKER
echo "Ingest directory:"
ls $ingestDir
ddtt=`date +%Y%m%d`
echo "===== End GINA product download: `date` ======"
) >> /awips2/edex/logs/edex-ingest-lclregsat-$ddtt".log" 2>&1
#
