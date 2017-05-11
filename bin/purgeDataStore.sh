#!/bin/bash
################################################
#  script to make sure raw data in the data_store 
#  directory doesn't fill up the file system
################################################
#
yyyymmdd=`date +%Y%m%d`
(
rawDir="/data_store/manual/regionalsat"
tdyDateStr=`date +%Y%m%d`
dirMin=2
MAX_VALUE=70
dircnt=`ls $rawDir | wc -w`
pct=` df -v | grep awips2 | cut -c 53-54`
#
echo "Directories: $dircnt   Disk usage: $pct (limit: $MAX_VALUE)"
if [ $pct -lt $MAX_VALUE ]
then
   echo "Sufficient disk space is still available...Nothing done"
   exit 0
elif [ $dircnt -le $dirMin ]
then
   echo "WARNING: Subdirectory size is too large: $rawDir"  
   echo "DISK IS NEARLY FULL! Unable to delete further without reconfiguring"
   exit 0
fi
#
echo "Disk is nearly full... deleting raw directories"
#
cnt=0
for dir in `ls -t $rawDir`
do
   (( cnt = cnt + 1 ))
   if [ "$tdyDateStr" = "$dir" ]
   then
      echo "Skip directory for today: $dir" 
   ##
   else
      if [ $cnt -gt $dirMin ]
      then 
         prefix=`echo $dir | cut -c 1-3`
         if [ "$prefix" = "201" ]
         then 
            echo "Remove $dir"
            rm -r $rawDir/$dir
            pct=` df -v | grep awips2 | cut -c 53-54`
            if [ $pct -lt $MAX_VALUE ]
            then
               echo "Sufficient disk space is now available... Exiting"
               exit 0
            fi 
         else
            echo "Unrecognized directory: $dir ... not removed!"
         fi
      else
         echo "Keep $dir"
      fi
   fi
done 
) >> /awips2/edex/logs/edex-purgedatastore-$yyyymmdd".log" 2>&1
