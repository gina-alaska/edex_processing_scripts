#!/bin/bash
###########################################
# script to make sure data is being purged
###########################################
#
ddtt=`date`
echo "------- `date` --------"
du -sh /data_store -sh
du -sh /awips2/edex/data/hdf5 
echo "---------------------------------------------"

