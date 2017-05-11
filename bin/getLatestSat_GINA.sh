#!/bin/bash
##################################
# chg to download directory
yyyymmdd=`date +%Y%m%d`
(
export PYTHONPATH=/awips2/fxa/bin/src:/awips2/python/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/awips2/python/lib
#
echo "+++++ Starting GINA product download - `date` ++++++"
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
baseDir="/awips2/data_store/download"
ingestDir="/awips2/edex/data/manual"
arglist=""
for var in "$@"
do
   if [ "$var" = "avhrr" -o "$var" = "metop" -o "$var" = "viirs" -o "$var" = "modis" ]
   then
      echo "Requesting: $var"
      arglist=$arglist" $var"
   else
      echo "Unknown datatype type ($var)!"
   fi    
done
#
if [ -z "$arglist" ]
then
   echo "No command line arguments. Default is all data types"
   echo ""
   arglist="viirs modis avhrr metop"  
fi
#
# check download directory for old files to clean up
#/home/awips/bin/myCleanup.py $baseDir -v
#
cd $baseDir
echo "/home/awips/bin/getGINAsat.py $arglist"
#/home/awips/bin/getGINAsat.py $arglist
/home/awips/bin/getGINAsatProd.py $arglist
#
#
touch UAF_marker
# next unzip and rename the files
for srcname in `ls UAF*`
do
   echo "File: $srcname"
   if [ "$srcname" = "UAF_marker" ]
   then
      rm $srcname
   else
      gunzip $srcname 
      srcname=`echo $srcname | sed 's/.gz//'`
      #srcname="${srcname%.*}"
      ##################################################
      # This section is for image quality check to be implemented later
      #qc_test=`/home/awips/bin/ncImageQC.py -c 60000 -r 50 $srcname`
      #tresult=`echo $qc_test | cut -c -4`
      ##################################################
      tresult="PASS"
      #pixelcnt=`/home/awips/bin/ncpixelcnt.py $srcname | cut -f1 -d' '`
      #if [ $pixelcnt -lt 60000 ]
      if [ "$tresult" = "FAIL" ]
      then
         echo "Image QC: $qc_test -  Removing $srcname"
         #mv $srcname /home/awips/tmp
         rm $srcname
      else
         destname="Alaska_$srcname"
         #mv $srcname $destname
         echo "mv $srcname $ingestDir/$destname"
         mv $srcname $ingestDir/$destname
      fi
   fi
done
#
echo "Ingest directory:"
ls $ingestDir
ddtt=`date +%Y%m%d`
echo "===== End GINA product download - `date` ======"
#
) >> /awips2/edex/logs/edex-ingest-lclregsat-$yyyymmdd".log" 2>&1
#
