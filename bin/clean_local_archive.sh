#!/bin/bash
##########################################
#
ddtt=`date +%Y%m%d`
(
echo "$ddtt Purging archive files..."
find /data_store/local/archive -name '*.h5' -mmin +360 -delete
find /data_store/local/archive -name '*.bin.*' -mmin +360 -delete
find /data_store/local/archive -empty -type d -delete
echo "Done"
#
) >> /awips2/edex/logs/edex-lclpurge-$ddtt".log" 2>&1
