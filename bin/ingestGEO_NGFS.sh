#!/bin/bash
###############################
#
ddtt=`date +%Y%m%d`
(
# chg to download directory
cd /data_store/download
echo "Checking for NGFS GEO: `date`"
shopt -s nullglob
for file in `ls NGFS_FIRE*`
do
   echo "Converting: $file"
   convertname=`/home/awips/bin/ncConvertNGFS_json.py -f $file | cut -c 17-`
   if [ -f $convertname ]
   then
      echo "Converted file: $convertname"
      mv $convertname /data_store/dropbox
      scp $convertname edex-test.x.gina.alaska.edu:/data_store/dropbox
      rm -f $file
   fi
done
) >> /awips2/edex/logs/edex-ingest-geo-ngfs-$ddtt".log" 2>&1
