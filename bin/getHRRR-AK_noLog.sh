#!/bin/bash
yyyymmdd=`date +%Y%m%d`
#(
SECONDS=0
LOCALDIR="/data_store/hrrr"
#SUBDIRS="wrfprs wrftwo wrfnat"
SUBDIRS="wrfnat"
#SUBDIRS="wrfprs wrftwo"
#USER="user"
#PASS="password"
LOG="/awips2/edex/logs/download_hrrr.log"
ingestDir=/awips2/edex/data/manual
#### this section determines the appropriate model cycle which occurs every 3 hours
ihr=`date +%k`
if [ $ihr -lt 2 ]
then
   (( ihr = ihr + 24 ))
fi
(( ihr = ihr - 2 ))
(( ihr = ihr / 3 ))
(( ihr = ihr * 3 ))
#############################
# next use year and julian from date command along with hour string to
# determine search string
chr=`printf '%02d' $ihr`
REGEX="`date +%y%j`"$chr"00[0-2]*"
echo "Downloading Hour: $REGEX"
#
# Now download the HRRR-AK model from the three subdirectories in the ESRL server
for subdir in $SUBDIRS
do
   # Make sure the destination directories exist
   if [ ! -d $LOCALDIR/$subdir ]
   then
      mkdir $LOCALDIR/$subdir
   fi
   #
   cd $LOCALDIR/$subdir
   rm *.$subdir.grb2
   # launch lftp
   # IS a timeout needed?  set net:timeout 3600
   lftp -u "anonymous,cfdierking@alaska.edu" gsdftp.fsl.noaa.gov:/hrrr_ak/alaska/$subdir << EOF
mirror -c -v -r --parallel=4 --include-glob $REGEX
bye
EOF
#mirror -c -v -r --parallel=4 --include-glob $REGEX
   #lftp -u "anonymous,cfdierking@alaska.edu" -e "mirror -c -v -r --parallel=4 --include-glob $REGEX;bye" gsdftp.fsl.noaa.gov:/hrrr_ak/alaska/$subdir
   #
   # rename to add the product type and grb2 extension
   for file in `ls $REGEX`
   do
      mv $file $file.$subdir."grb2"
   done
   # send to the EDEX manual ingest directory
   cp *.$subdir.grb2 $ingestDir
done
#
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds to download."
echo "Done"
#) >> /awips2/edex/logs/edex-ingest-hrrr-$yyyymmdd".log" 2>&1
